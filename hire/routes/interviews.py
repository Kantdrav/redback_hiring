from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import db, Round, Interview, Candidate, MCQQuestion
from services.interview_engine import schedule_interview, record_assessment
from services.mcq_engine import grade_mcq
from datetime import datetime, timezone
import json

interviews_bp = Blueprint("interviews", __name__, template_folder="../templates/interviews")

@interviews_bp.route("/plans")
@login_required
@role_required("admin","hr")
def plans():
    rounds = Round.query.order_by(Round.order_index).all()
    return render_template("interviews/plans.html", rounds=rounds)

@interviews_bp.route("/round/create", methods=["GET","POST"])
@login_required
@role_required("admin","hr")
def create_round():
    if request.method == "POST":
        name = request.form.get("name")
        rtype = request.form.get("type")
        duration = int(request.form.get("duration") or 30)
        order_index = int(request.form.get("order_index") or 0)
        config = request.form.get("config_json") or "{}"
        r = Round(name=name, type=rtype, duration_minutes=duration, order_index=order_index, config_json=config)
        db.session.add(r)
        db.session.commit()
        flash("Round created", "success")
        return redirect(url_for("interviews.plans"))
    return render_template("interviews/create_round.html")

@interviews_bp.route("/schedule", methods=["GET","POST"])
@login_required
@role_required("admin","hr")
def schedule():
    if request.method == "POST":
        round_id = int(request.form.get("round_id"))
        candidate_id = int(request.form.get("candidate_id"))
        interviewer_id = int(request.form.get("interviewer_id"))
        dt_str = request.form.get("scheduled_at")  # expect ISO 8601 (UTC) or local -> convert
        # Parse naive datetime; user should send in UTC or convert server-side
        scheduled_at_utc = datetime.fromisoformat(dt_str)
        duration = int(request.form.get("duration") or 30)
        iv = Interview(round_id=round_id, candidate_id=candidate_id, interviewer_id=interviewer_id, scheduled_at_utc=scheduled_at_utc, duration=duration)
        db.session.add(iv)
        db.session.commit()
        flash("Interview scheduled", "success")
        return redirect(url_for("interviews.plans"))
    rounds = Round.query.all()
    from models.job import Job
    candidates = Candidate.query.order_by(Candidate.created_at.desc()).limit(50).all()
    # for interviewer list, find users with role 'interviewer'
    from models.user import User
    interviewers = User.query.filter(User.role=="interviewer").all()
    return render_template("interviews/schedule_interview.html", rounds=rounds, candidates=candidates, interviewers=interviewers)

@interviews_bp.route("/dashboard")
@login_required
def interviewer_dashboard():
    # Interviewer sees assigned interviews
    if current_user.role != "interviewer":
        flash("Only interviewers can view this page", "danger")
        return redirect(url_for("jobs.list_jobs"))
    
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
    
    return render_template("interviews/interviewer_dashboard.html", 
                          stats=stats, 
                          recent_interviews=recent_interviews)

@interviews_bp.route("/execute/<int:interview_id>", methods=["GET","POST"])
@login_required
def execute(interview_id):
    iv = Interview.query.get_or_404(interview_id)
    
    # permission: assigned interviewer, candidate taking the interview, hr/admin
    is_interviewer = current_user.id == iv.interviewer_id
    
    # Check if candidate is the current user - by user_id OR by email match
    is_candidate = False
    if current_user.role == "candidate" and iv.candidate:
        # Check by user_id if it exists
        if iv.candidate.user_id == current_user.id:
            is_candidate = True
        # Fallback: check by email match
        elif iv.candidate.email == current_user.email:
            is_candidate = True
    
    is_admin_or_hr = current_user.role in ("admin", "hr")
    
    if not (is_interviewer or is_candidate or is_admin_or_hr):
        flash("Not authorized to execute this interview", "danger")
        # Redirect based on user role
        if current_user.role == "candidate":
            return redirect(url_for("candidate.view_interviews"))
        else:
            return redirect(url_for("interviews.interviewer_dashboard"))
    
    if request.method == "POST":
        # endpoint to submit assessment
        score_numeric = request.form.get("score_numeric")
        feedback = request.form.get("feedback")
        score_json = request.form.get("score_json") or "{}"
        a = record_assessment(interview_id=iv.id, submitted_by=current_user.id, score_numeric=float(score_numeric) if score_numeric else None, score_json=score_json, feedback_text=feedback)
        flash("Assessment saved", "success")
        return redirect(url_for("interviews.interviewer_dashboard"))
    # if round is MCQ, provide link to take test
    rnd = iv.round
    mcq_questions = []
    if rnd and rnd.type == "mcq":
        mcq_questions = MCQQuestion.query.filter_by(round_id=rnd.id).all()
    return render_template("interviews/execute_interview.html", interview=iv, mcq_questions=mcq_questions)

# MCQ/Quiz endpoints
@interviews_bp.route("/quizzes")
@login_required
@role_required("admin","hr","interviewer")
def list_quizzes():
    """List all available rounds for creating quizzes"""
    rounds = Round.query.order_by(Round.order_index).all()
    return render_template("interviews/quiz_list.html", rounds=rounds)


@interviews_bp.route("/quiz/create", methods=["GET","POST"])
@login_required
@role_required("admin","hr","interviewer")
def create_round_for_quiz():
    """Create a new quiz/round"""
    if request.method == "POST":
        name = request.form.get("name")
        rtype = request.form.get("type")
        duration = int(request.form.get("duration") or 30)
        config = request.form.get("config_json") or "{}"
        
        r = Round(name=name, type=rtype, duration_minutes=duration, order_index=0, config_json=config)
        db.session.add(r)
        db.session.commit()
        
        flash(f"Quiz '{name}' created successfully", "success")
        return redirect(url_for("interviews.quiz_questions", round_id=r.id))
    
    return render_template("interviews/create_quiz.html")


@interviews_bp.route("/quiz/<int:round_id>/questions")
@login_required
@role_required("admin","hr","interviewer")
def quiz_questions(round_id):
    """View and manage questions for a quiz"""
    round_info = Round.query.get_or_404(round_id)
    questions = MCQQuestion.query.filter_by(round_id=round_id).all()
    return render_template("interviews/quiz_questions.html", round=round_info, questions=questions)


@interviews_bp.route("/mcq/<int:round_id>/create", methods=["GET","POST"])
@login_required
@role_required("admin","hr","interviewer")
def mcq_create(round_id):
    """Add MCQ question to a round/quiz"""
    round_info = Round.query.get_or_404(round_id)
    
    if request.method == "POST":
        qtext = request.form.get("question_text")
        choices_raw = request.form.getlist("choices")
        correct_index = int(request.form.get("correct_index") or 0)
        marks = float(request.form.get("marks") or 1.0)
        
        q = MCQQuestion(round_id=round_id, question_text=qtext, choices_json=json.dumps(choices_raw), correct_index=correct_index, marks=marks)
        db.session.add(q)
        db.session.commit()
        
        flash("MCQ question added", "success")
        return redirect(url_for("interviews.quiz_questions", round_id=round_id))
    
    return render_template("interviews/mcq_create.html", round_id=round_id, round=round_info)


@interviews_bp.route("/mcq/<int:question_id>/edit", methods=["GET","POST"])
@login_required
@role_required("admin","hr","interviewer")
def edit_mcq(question_id):
    """Edit an MCQ question"""
    q = MCQQuestion.query.get_or_404(question_id)
    round_id = q.round_id
    round_info = Round.query.get(round_id)
    
    if request.method == "POST":
        q.question_text = request.form.get("question_text")
        q.choices_json = json.dumps(request.form.getlist("choices"))
        q.correct_index = int(request.form.get("correct_index") or 0)
        q.marks = float(request.form.get("marks") or 1.0)
        db.session.commit()
        
        flash("Question updated", "success")
        return redirect(url_for("interviews.quiz_questions", round_id=round_id))
    
    choices = q.get_choices()
    return render_template("interviews/edit_mcq.html", question=q, round=round_info, round_id=round_id, choices=choices)


@interviews_bp.route("/mcq/<int:question_id>/delete", methods=["POST"])
@login_required
@role_required("admin","hr","interviewer")
def delete_mcq(question_id):
    """Delete an MCQ question"""
    q = MCQQuestion.query.get_or_404(question_id)
    round_id = q.round_id
    db.session.delete(q)
    db.session.commit()
    
    flash("Question deleted", "success")
    return redirect(url_for("interviews.quiz_questions", round_id=round_id))

@interviews_bp.route("/mcq/take/<int:round_id>", methods=["GET","POST"])
@login_required
def mcq_take(round_id):
    # candidate taking the MCQ as part of an interview flow
    # find the interview for this candidate & round where status is scheduled or in-progress
    # map logged-in user -> Candidate profile
    candidate_profile = None
    try:
        if hasattr(current_user, "role") and current_user.role == "candidate":
            candidate_profile = Candidate.query.filter_by(user_id=current_user.id).first()
    except Exception:
        candidate_profile = None

    iv = None
    if candidate_profile is not None:
        iv = Interview.query.filter_by(round_id=round_id, candidate_id=candidate_profile.id)\
            .order_by(Interview.scheduled_at_utc.desc()).first()
    if not iv:
        flash("No active interview found for this round", "danger")
        return redirect(url_for("jobs.list_jobs"))
    qs = MCQQuestion.query.filter_by(round_id=round_id).all()
    if request.method == "POST":
        answers = {}
        for q in qs:
            val = request.form.get(f"q_{q.id}")
            if val is not None:
                answers[str(q.id)] = int(val)
        res = grade_mcq(round_id, answers)
        # save assessment record
        from services.interview_engine import record_assessment
        a = record_assessment(interview_id=iv.id, submitted_by=current_user.id, score_numeric=res["obtained_marks"], score_json=json.dumps(res), feedback_text="MCQ Auto-graded")
        flash("MCQ submitted. Score: {} / {}".format(res["obtained_marks"], res["total_marks"]), "success")
        return redirect(url_for("jobs.list_jobs"))
    return render_template("interviews/mcq_take.html", questions=qs, round_id=round_id)


@interviews_bp.route("/mcq/take/interview/<int:interview_id>", methods=["GET","POST"])
@login_required
def mcq_take_interview(interview_id):
    """Take MCQ test for a specific interview"""
    iv = Interview.query.get_or_404(interview_id)
    
    # Check authorization - candidate or interviewer
    is_candidate = False
    if current_user.role == "candidate" and iv.candidate:
        if iv.candidate.user_id == current_user.id or iv.candidate.email == current_user.email:
            is_candidate = True
    
    is_interviewer = current_user.id == iv.interviewer_id
    is_admin_or_hr = current_user.role in ("admin", "hr")
    
    if not (is_candidate or is_interviewer or is_admin_or_hr):
        flash("Not authorized to take this test", "danger")
        return redirect(url_for("candidate.view_interviews") if current_user.role == "candidate" else url_for("interviews.interviewer_dashboard"))
    
    round_id = iv.round_id
    qs = MCQQuestion.query.filter_by(round_id=round_id).all()
    
    if not qs:
        flash("No questions available for this quiz", "warning")
        return redirect(url_for("interviews.execute", interview_id=interview_id))
    
    if request.method == "POST":
        answers = {}
        for q in qs:
            val = request.form.get(f"q_{q.id}")
            if val is not None:
                answers[str(q.id)] = int(val)
        
        res = grade_mcq(round_id, answers)
        
        # Save assessment record
        a = record_assessment(
            interview_id=iv.id, 
            submitted_by=current_user.id, 
            score_numeric=res["obtained_marks"], 
            score_json=json.dumps(res), 
            feedback_text="MCQ Auto-graded"
        )
        
        # Update interview status to completed
        iv.status = "completed"
        db.session.commit()
        
        flash(f"MCQ submitted. Score: {res['obtained_marks']} / {res['total_marks']}", "success")
        
        # Redirect to results page
        return redirect(url_for("interviews.view_assessment_results", interview_id=interview_id))
    
    return render_template("interviews/mcq_take.html", questions=qs, round_id=round_id, interview=iv)


@interviews_bp.route("/assessment/<int:interview_id>/results")
@login_required
def view_assessment_results(interview_id):
    """View detailed assessment results with candidate answers"""
    from models import Assessment, MCQQuestion
    
    iv = Interview.query.get_or_404(interview_id)
    
    # Authorization check: allow candidate, any interviewer role, admin/HR
    is_candidate = False
    if current_user.role == "candidate" and iv.candidate:
        if iv.candidate.user_id == current_user.id or iv.candidate.email == current_user.email:
            is_candidate = True

    role = getattr(current_user, "role", None)
    is_interviewer_role = role == "interviewer"
    is_admin_or_hr = role in ("admin", "hr")

    if not (is_candidate or is_interviewer_role or is_admin_or_hr):
        flash("Not authorized to view these results", "danger")
        return redirect(url_for("interviews.interviewer_dashboard") if role == "interviewer" else url_for("candidate.view_interviews"))
    
    assessment = Assessment.query.filter_by(interview_id=interview_id).first()
    if not assessment:
        flash("No assessment found for this interview", "warning")
        return redirect(url_for("interviews.interviewer_dashboard") if current_user.role == "interviewer" else url_for("candidate.view_interviews"))
    
    # Parse score details
    score_detail = assessment.get_score_json()
    detail = score_detail.get("detail", {})
    answers = score_detail.get("answers", {})
    total_marks = score_detail.get("total_marks", 0)
    obtained_marks = score_detail.get("obtained_marks", 0)
    percentage = (obtained_marks / total_marks * 100) if total_marks > 0 else 0
    
    # Determine pass/fail status (assuming 40% is passing)
    passed_status = "PASSED ✓" if percentage >= 40 else "FAILED ✗"
    
    # Get all questions for this round (ordered by creation)
    questions = MCQQuestion.query.filter_by(round_id=iv.round_id).order_by(MCQQuestion.id).all()
    
    # Parse candidate answers from score_json
    candidate_answers = {}
    for q in questions:
        q_str = str(q.id)
        if q_str in answers:
            candidate_answers[q.id] = int(answers[q_str])
    
    return render_template("interviews/assessment_results.html",
                          interview=iv,
                          assessment=assessment,
                          score_detail=detail,
                          total_marks=total_marks,
                          obtained_marks=obtained_marks,
                          percentage=percentage,
                          passed_status=passed_status,
                          questions=questions,
                          candidate_answers=candidate_answers)
