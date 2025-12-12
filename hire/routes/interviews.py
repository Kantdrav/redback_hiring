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
    invs = Interview.query.filter_by(interviewer_id=current_user.id).order_by(Interview.scheduled_at_utc.asc()).all()
    return render_template("interviews/interviewer_dashboard.html", interviews=invs)

@interviews_bp.route("/execute/<int:interview_id>", methods=["GET","POST"])
@login_required
def execute(interview_id):
    iv = Interview.query.get_or_404(interview_id)
    # permission: assigned interviewer or hr/admin
    if current_user.role not in ("admin","hr") and current_user.id != iv.interviewer_id:
        flash("Not authorized to execute this interview", "danger")
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

# MCQ endpoints
@interviews_bp.route("/mcq/<int:round_id>/create", methods=["GET","POST"])
@login_required
@role_required("admin","hr")
def mcq_create(round_id):
    if request.method == "POST":
        qtext = request.form.get("question_text")
        choices_raw = request.form.getlist("choices")
        correct_index = int(request.form.get("correct_index") or 0)
        marks = float(request.form.get("marks") or 1.0)
        from models.mcq_question import MCQQuestion
        q = MCQQuestion(round_id=round_id, question_text=qtext, choices_json=json.dumps(choices_raw), correct_index=correct_index, marks=marks)
        db.session.add(q)
        db.session.commit()
        flash("MCQ question added", "success")
        return redirect(url_for("interviews.execute", interview_id=request.args.get("interview_id") or 0))
    return render_template("interviews/mcq_create.html", round_id=round_id)

@interviews_bp.route("/mcq/take/<int:round_id>", methods=["GET","POST"])
@login_required
def mcq_take(round_id):
    # candidate taking the MCQ as part of an interview flow
    # find the interview for this candidate & round where status is scheduled or in-progress
    iv = Interview.query.filter_by(round_id=round_id, candidate_id=current_user.id).order_by(Interview.scheduled_at_utc.desc()).first()
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
