"""Interviewer Dashboard - View assigned interviews, grade tasks, review results"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import (
    db, Interview, Assessment, CandidateTestResult, InterviewSchedule, 
    Candidate, Round, AuditLog
)
from datetime import datetime
import json

interviewer_bp = Blueprint("interviewer", __name__, template_folder="../templates/interviewer")


# ==================== INTERVIEWER DASHBOARD ====================
@interviewer_bp.route("/dashboard")
@login_required
@role_required("interviewer")
def dashboard():
    """Main interviewer dashboard"""
    assigned_interviews = Interview.query.filter_by(interviewer_id=current_user.id).all()
    pending_count = len([i for i in assigned_interviews if i.status == "scheduled"])
    completed_count = len([i for i in assigned_interviews if i.status == "completed"])
    
    stats = {
        "total_assigned": len(assigned_interviews),
        "pending": pending_count,
        "completed": completed_count
    }
    
    recent_interviews = Interview.query.filter_by(interviewer_id=current_user.id)\
        .order_by(Interview.scheduled_at_utc.desc()).limit(10).all()
    
    return render_template("interviewer/dashboard.html", 
                          stats=stats, 
                          recent_interviews=recent_interviews)


# ==================== ASSIGNED INTERVIEWS ====================
@interviewer_bp.route("/interviews")
@login_required
@role_required("interviewer")
def list_interviews():
    """List all assigned interviews"""
    status_filter = request.args.get("status", "all")
    
    query = Interview.query.filter_by(interviewer_id=current_user.id)
    
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
    
    interviews = query.order_by(Interview.scheduled_at_utc.desc()).all()
    return render_template("interviewer/interviews_list.html", 
                          interviews=interviews, 
                          current_status=status_filter)


@interviewer_bp.route("/interviews/<int:interview_id>")
@login_required
@role_required("interviewer")
def view_interview(interview_id):
    """View interview details"""
    interview = Interview.query.get_or_404(interview_id)
    
    # Check authorization
    if interview.interviewer_id != current_user.id:
        flash("You don't have permission to view this interview", "danger")
        return redirect(url_for("interviewer.list_interviews"))
    
    assessment = Assessment.query.filter_by(interview_id=interview_id).first()
    round_info = Round.query.get(interview.round_id) if interview.round_id else None
    
    return render_template("interviewer/interview_detail.html", 
                          interview=interview, 
                          assessment=assessment,
                          round_info=round_info)


# ==================== GRADING & ASSESSMENT ====================
@interviewer_bp.route("/interviews/<int:interview_id>/grade", methods=["GET", "POST"])
@login_required
@role_required("interviewer")
def grade_interview(interview_id):
    """Grade an interview (manual task grading)"""
    interview = Interview.query.get_or_404(interview_id)
    
    # Check authorization
    if interview.interviewer_id != current_user.id:
        flash("You don't have permission to grade this interview", "danger")
        return redirect(url_for("interviewer.list_interviews"))
    
    assessment = Assessment.query.filter_by(interview_id=interview_id).first()
    
    if request.method == "POST":
        score = request.form.get("score", type=float)
        feedback = request.form.get("feedback", "").strip()
        
        if score is None or score < 0 or score > 100:
            flash("Score must be between 0 and 100", "danger")
            return redirect(url_for("interviewer.grade_interview", interview_id=interview_id))
        
        if not assessment:
            assessment = Assessment(interview_id=interview_id)
            db.session.add(assessment)
        
        assessment.score_numeric = score
        assessment.feedback_text = feedback
        assessment.submitted_by = current_user.id
        assessment.submitted_at = datetime.utcnow()
        
        # Update interview status to completed
        interview.status = "completed"
        
        db.session.commit()
        
        log_interviewer_action("grade", "interview", interview_id, current_user.id, 
                              {"score": score})
        
        flash("Interview graded successfully", "success")
        return redirect(url_for("interviewer.view_interview", interview_id=interview_id))
    
    return render_template("interviewer/grade_interview.html", 
                          interview=interview, 
                          assessment=assessment)


# ==================== TEST RESULTS & REVIEW ====================
@interviewer_bp.route("/test-results")
@login_required
@role_required("interviewer")
def list_test_results():
    """List test results for review"""
    # Get interviews where interviewer can review auto-graded results
    interviews = Interview.query.filter_by(interviewer_id=current_user.id).all()
    interview_ids = [i.id for i in interviews]
    
    # Get test results from these interviews
    test_results = CandidateTestResult.query\
        .filter(CandidateTestResult.interview_schedule_id.in_(interview_ids))\
        .order_by(CandidateTestResult.submitted_at.desc()).all()
    
    return render_template("interviewer/test_results_list.html", 
                          test_results=test_results)


@interviewer_bp.route("/test-results/<int:result_id>")
@login_required
@role_required("interviewer")
def view_test_result(result_id):
    """View and review test result"""
    result = CandidateTestResult.query.get_or_404(result_id)
    
    # Verify authorization
    schedule = InterviewSchedule.query.get(result.interview_schedule_id)
    
    if not schedule:
        flash("Test result not found", "danger")
        return redirect(url_for("interviewer.list_test_results"))
    
    # Check if interviewer is assigned to this candidate's interview
    interview = Interview.query.filter_by(
        candidate_id=schedule.candidate_id,
        interviewer_id=current_user.id
    ).first()
    
    if not interview:
        flash("You don't have permission to review this test", "danger")
        return redirect(url_for("interviewer.list_test_results"))
    
    test_data = json.loads(result.test_data_json or "{}")
    
    return render_template("interviewer/test_result_detail.html", 
                          result=result, 
                          test_data=test_data)


@interviewer_bp.route("/test-results/<int:result_id>/review", methods=["POST"])
@login_required
@role_required("interviewer")
def review_test_result(result_id):
    """Add reviewer comments to auto-graded test"""
    result = CandidateTestResult.query.get_or_404(result_id)
    
    review_status = request.form.get("review_status")  # accepted, needs_discussion, rejected
    reviewer_comments = request.form.get("comments", "").strip()
    
    if review_status not in ["accepted", "needs_discussion", "rejected"]:
        flash("Invalid review status", "danger")
        return redirect(url_for("interviewer.view_test_result", result_id=result_id))
    
    # Store review in test_data
    test_data = json.loads(result.test_data_json or "{}")
    if "reviews" not in test_data:
        test_data["reviews"] = []
    
    test_data["reviews"].append({
        "reviewed_by": current_user.name,
        "reviewed_at": datetime.utcnow().isoformat(),
        "status": review_status,
        "comments": reviewer_comments
    })
    
    result.test_data_json = json.dumps(test_data)
    result.status = review_status
    db.session.commit()
    
    log_interviewer_action("review", "test_result", result_id, current_user.id, 
                          {"status": review_status})
    
    flash("Test review submitted successfully", "success")
    return redirect(url_for("interviewer.view_test_result", result_id=result_id))


# ==================== CODING SUBMISSIONS ====================
@interviewer_bp.route("/coding-submissions")
@login_required
@role_required("interviewer")
def list_coding_submissions():
    """List coding submissions for technical rounds"""
    # Get interviews where interviewer can review coding submissions
    interviews = Interview.query.filter_by(interviewer_id=current_user.id).all()
    interview_ids = [i.id for i in interviews]
    
    # Get test results marked as coding submissions
    submissions = CandidateTestResult.query\
        .filter(CandidateTestResult.interview_schedule_id.in_(interview_ids))\
        .filter_by(round_type="coding")\
        .order_by(CandidateTestResult.submitted_at.desc()).all()
    
    return render_template("interviewer/coding_submissions_list.html", 
                          submissions=submissions)


@interviewer_bp.route("/coding-submissions/<int:submission_id>")
@login_required
@role_required("interviewer")
def view_coding_submission(submission_id):
    """View coding submission with code"""
    result = CandidateTestResult.query.get_or_404(submission_id)
    test_data = json.loads(result.test_data_json or "{}")
    
    return render_template("interviewer/coding_submission_detail.html", 
                          submission=result, 
                          code=test_data.get("code_submitted", ""),
                          language=result.language_tested)


# ==================== HELPER FUNCTIONS ====================
def log_interviewer_action(action, entity_type, entity_id, user_id, payload=None):
    """Log interviewer action to audit log"""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        payload_json=json.dumps(payload) if payload else None
    )
    db.session.add(log)
    db.session.commit()
