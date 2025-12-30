"""Candidate Dashboard - Apply for jobs, view interviews, take tests, see results"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import (
    db, Candidate, Job, InterviewSchedule, InterviewPlan, 
    CandidateTestResult, AuditLog
)
from datetime import datetime
import json

candidate_bp = Blueprint("candidate", __name__, template_folder="../templates/candidate")


# ==================== CANDIDATE DASHBOARD ====================
@candidate_bp.route("/dashboard")
@login_required
@role_required("candidate")
def dashboard():
    """Main candidate dashboard"""
    # Get or create candidate profile
    candidate = get_or_create_candidate()
    
    applied_jobs = Job.query.filter_by(status="open").count()
    my_applications = Candidate.query.filter_by(user_id=current_user.id).all()
    
    # Get interview schedules for this candidate
    schedules = InterviewSchedule.query\
        .filter(InterviewSchedule.candidate_id.in_([c.id for c in my_applications]))\
        .order_by(InterviewSchedule.invited_at.desc()).all()
    
    pending_schedules = [s for s in schedules if s.status in ["invited", "in_progress"]]
    completed_schedules = [s for s in schedules if s.status == "completed"]
    
    stats = {
        "open_jobs": applied_jobs,
        "my_applications": len(my_applications),
        "pending_interviews": len(pending_schedules),
        "completed_interviews": len(completed_schedules)
    }
    
    # Build map of schedule_id -> mcq_round_id for quick access in template
    mcq_round_map = {}
    try:
        from models.round import Round
        for s in pending_schedules:
            try:
                plan = s.interview_plan
                rounds = plan.get_rounds() if plan else []
                current_round = rounds[s.current_round_index] if s.current_round_index < len(rounds) else None
                if current_round and current_round.get("type") == "mcq":
                    q = Round.query.filter(Round.type == "mcq")
                    if current_round.get("name"):
                        q = q.filter(Round.name == current_round.get("name"))
                    match = q.order_by(Round.created_at.desc()).first()
                    if match:
                        mcq_round_map[s.id] = match.id
            except Exception:
                continue
    except Exception:
        mcq_round_map = {}

    return render_template("candidate/dashboard.html", 
                          stats=stats,
                          candidate=candidate,
                          pending_interviews=pending_schedules,
                          completed_interviews=completed_schedules,
                          mcq_round_map=mcq_round_map)


# ==================== JOB APPLICATIONS ====================
@candidate_bp.route("/job-board")
@login_required
@role_required("candidate")
def job_board():
    """Browse and apply for open jobs"""
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "")
    
    query = Job.query.filter_by(status="open")
    
    if search:
        query = query.filter(
            (Job.title.ilike(f"%{search}%")) | 
            (Job.description.ilike(f"%{search}%"))
        )
    
    jobs = query.order_by(Job.created_at.desc()).paginate(page=page, per_page=10)
    
    # Get candidate's applications
    candidate = Candidate.query.filter_by(user_id=current_user.id).all()
    applied_job_ids = [c.applied_job_id for c in candidate]
    
    return render_template("candidate/job_board.html", 
                          jobs=jobs, 
                          applied_job_ids=applied_job_ids,
                          search=search)


@candidate_bp.route("/apply/<int:job_id>", methods=["POST"])
@login_required
@role_required("candidate")
def apply_for_job(job_id):
    """Apply for a job"""
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing = Candidate.query.filter_by(
        user_id=current_user.id,
        applied_job_id=job_id
    ).first()
    
    if existing:
        flash("You have already applied for this job", "warning")
        return redirect(url_for("candidate.job_board"))
    
    # Create application
    candidate = Candidate(
        user_id=current_user.id,
        name=getattr(current_user, "name", current_user.email),
        email=current_user.email,
        phone=getattr(current_user, "phone", None),
        applied_job_id=job_id,
        status="applied"
    )
    db.session.add(candidate)
    db.session.commit()
    
    log_candidate_action("apply", "job", job_id, current_user.id, {"job_title": job.title})
    flash(f"Successfully applied for {job.title}", "success")
    return redirect(url_for("candidate.job_board"))


@candidate_bp.route("/my-applications")
@login_required
@role_required("candidate")
def my_applications():
    """View my job applications"""
    applications = Candidate.query.filter_by(user_id=current_user.id).all()
    return render_template("candidate/my_applications.html", applications=applications)


# ==================== INTERVIEW SCHEDULES ====================
@candidate_bp.route("/interviews")
@login_required
@role_required("candidate")
def view_interviews():
    """View scheduled interviews"""
    from models import Interview
    
    candidate = Candidate.query.filter_by(user_id=current_user.id).all()
    candidate_ids = [c.id for c in candidate]
    
    # Get both InterviewSchedule and Interview records
    schedules = InterviewSchedule.query\
        .filter(InterviewSchedule.candidate_id.in_(candidate_ids))\
        .order_by(InterviewSchedule.invited_at.desc()).all()
    
    # Get Interview records assigned by interviewers
    interviews = Interview.query\
        .filter(Interview.candidate_id.in_(candidate_ids))\
        .order_by(Interview.created_at.desc()).all()

    # Build map of schedule_id -> mcq_round_id when current round is mcq
    mcq_round_map = {}
    try:
        from models.round import Round
        for s in schedules:
            try:
                plan = s.interview_plan
                rounds = plan.get_rounds() if plan else []
                current_round = rounds[s.current_round_index] if s.current_round_index < len(rounds) else None
                if current_round and current_round.get("type") == "mcq":
                    q = Round.query.filter(Round.type == "mcq")
                    if current_round.get("name"):
                        q = q.filter(Round.name == current_round.get("name"))
                    match = q.order_by(Round.created_at.desc()).first()
                    if match:
                        mcq_round_map[s.id] = match.id
            except Exception:
                continue
    except Exception:
        mcq_round_map = {}

    return render_template("candidate/interviews_list.html", 
                          schedules=schedules, 
                          interviews=interviews,
                          mcq_round_map=mcq_round_map)


@candidate_bp.route("/interviews/<int:schedule_id>/accept", methods=["POST"])
@login_required
@role_required("candidate")
def accept_interview(schedule_id):
    """Accept interview invitation"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    
    # Verify candidate authorization
    candidate = Candidate.query.get(schedule.candidate_id)
    if candidate.user_id != current_user.id:
        flash("You don't have permission to accept this interview", "danger")
        return redirect(url_for("candidate.view_interviews"))
    
    if schedule.status != "invited":
        flash("This interview is not available for acceptance", "warning")
        return redirect(url_for("candidate.view_interviews"))
    
    schedule.status = "in_progress"
    schedule.started_at = datetime.utcnow()
    db.session.commit()
    
    log_candidate_action("accept", "interview_schedule", schedule_id, current_user.id)
    flash("Interview invitation accepted", "success")
    return redirect(url_for("candidate.view_interviews"))


@candidate_bp.route("/interviews/<int:schedule_id>/decline", methods=["POST"])
@login_required
@role_required("candidate")
def decline_interview(schedule_id):
    """Decline interview invitation"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    
    # Verify candidate authorization
    candidate = Candidate.query.get(schedule.candidate_id)
    if candidate.user_id != current_user.id:
        flash("You don't have permission to decline this interview", "danger")
        return redirect(url_for("candidate.view_interviews"))
    
    if schedule.status != "invited":
        flash("This interview cannot be declined at this stage", "warning")
        return redirect(url_for("candidate.view_interviews"))
    
    schedule.status = "rejected"
    db.session.commit()
    
    log_candidate_action("decline", "interview_schedule", schedule_id, current_user.id)
    flash("Interview invitation declined", "success")
    return redirect(url_for("candidate.view_interviews"))


# ==================== TEST TAKING ====================
@candidate_bp.route("/test/<int:schedule_id>")
@login_required
@role_required("candidate")
def take_test(schedule_id):
    """Take interview test/assessment"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    
    # Verify candidate authorization
    candidate = Candidate.query.get(schedule.candidate_id)
    if candidate.user_id != current_user.id:
        flash("You don't have permission to take this test", "danger")
        return redirect(url_for("candidate.view_interviews"))
    
    if schedule.status != "in_progress":
        flash("This interview is not ready for testing", "warning")
        return redirect(url_for("candidate.view_interviews"))
    
    # Get interview plan rounds
    plan = schedule.interview_plan
    rounds = plan.get_rounds()
    current_round = rounds[schedule.current_round_index] if schedule.current_round_index < len(rounds) else None
    
    # Resolve MCQ round id and questions if current round is MCQ
    mcq_round_id = None
    mcq_questions = []
    try:
        if current_round and current_round.get("type") == "mcq":
            from models.round import Round
            from models.mcq_question import MCQQuestion
            q = Round.query.filter(Round.type == "mcq")
            # Prefer name match when available
            if current_round.get("name"):
                q = q.filter(Round.name == current_round.get("name"))
            match = q.order_by(Round.created_at.desc()).first()
            if match:
                mcq_round_id = match.id
                # Load MCQ questions for this round
                mcq_questions = MCQQuestion.query.filter_by(round_id=mcq_round_id).all()
    except Exception:
        mcq_round_id = None
        mcq_questions = []

    return render_template("candidate/take_test.html", 
                          schedule=schedule, 
                          plan=plan,
                          current_round=current_round,
                          round_index=schedule.current_round_index,
                          mcq_round_id=mcq_round_id,
                          mcq_questions=mcq_questions)


@candidate_bp.route("/test/<int:schedule_id>/submit", methods=["POST"])
@login_required
@role_required("candidate")
def submit_test(schedule_id):
    """Submit test responses"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    
    # Verify candidate authorization
    candidate = Candidate.query.get(schedule.candidate_id)
    if candidate.user_id != current_user.id:
        flash("You don't have permission to submit this test", "danger")
        return redirect(url_for("candidate.view_interviews"))
    
    # Get responses from form
    round_index = request.form.get("round_index", type=int)
    responses = {}
    
    # Collect all question responses
    for key, value in request.form.items():
        if key.startswith("question_"):
            q_id = key.replace("question_", "")
            responses[q_id] = value
    
    # Create test result
    result = CandidateTestResult(
        interview_schedule_id=schedule_id,
        round_index=round_index,
        test_data_json=json.dumps({"responses": responses}),
        status="pending_review"
    )
    db.session.add(result)
    
    # Move to next round or mark as completed
    plan = schedule.interview_plan
    rounds = plan.get_rounds()
    
    if round_index + 1 < len(rounds):
        schedule.current_round_index = round_index + 1
    else:
        schedule.status = "completed"
        schedule.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    log_candidate_action("submit", "test", result.id, current_user.id)
    flash("Test submitted successfully", "success")
    return redirect(url_for("candidate.view_interview_outcome", schedule_id=schedule_id))


# ==================== RESULTS & FEEDBACK ====================
@candidate_bp.route("/interview/<int:schedule_id>/outcome")
@login_required
@role_required("candidate")
def view_interview_outcome(schedule_id):
    """View interview results and feedback"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    
    # Verify candidate authorization
    candidate = Candidate.query.get(schedule.candidate_id)
    if candidate.user_id != current_user.id:
        flash("You don't have permission to view this outcome", "danger")
        return redirect(url_for("candidate.view_interviews"))
    
    test_results = CandidateTestResult.query\
        .filter_by(interview_schedule_id=schedule_id)\
        .order_by(CandidateTestResult.submitted_at.desc()).all()
    
    feedback = json.loads(schedule.feedback_json or "{}")
    
    return render_template("candidate/interview_outcome.html", 
                          schedule=schedule, 
                          test_results=test_results,
                          feedback=feedback)


# ==================== HELPER FUNCTIONS ====================
def get_or_create_candidate():
    """Get or create candidate profile for current user"""
    candidate = Candidate.query.filter_by(user_id=current_user.id).first()
    
    if not candidate:
        candidate = Candidate(
            user_id=current_user.id,
            name=getattr(current_user, "name", current_user.email),
            email=current_user.email,
            phone=getattr(current_user, "phone", None),
            status="profile_created"
        )
        db.session.add(candidate)
        db.session.commit()
    
    return candidate


def log_candidate_action(action, entity_type, entity_id, user_id, payload=None):
    """Log candidate action to audit log"""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        payload_json=json.dumps(payload) if payload else None
    )
    db.session.add(log)
    db.session.commit()
