"""HR Dashboard - Manage job openings, interview plans, candidate invitations"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import (
    db, Job, InterviewPlan, InterviewSchedule, Candidate, 
    ProgrammingLanguage, RoundTemplate, AuditLog
)
from datetime import datetime
import json

hr_jobs_bp = Blueprint("hr_jobs", __name__, template_folder="../templates/hr")


# ==================== HR DASHBOARD MAIN ====================
@hr_jobs_bp.route("/dashboard")
@login_required
@role_required("admin", "hr")
def dashboard():
    """Main HR dashboard with overview"""
    open_jobs = Job.query.filter_by(status="open", created_by=current_user.id).count()
    active_plans = InterviewPlan.query.filter_by(status="active").count()
    pending_interviews = InterviewSchedule.query.filter_by(status="invited").count()
    
    stats = {
        "open_jobs": open_jobs,
        "active_plans": active_plans,
        "pending_interviews": pending_interviews
    }
    
    recent_jobs = Job.query.filter_by(created_by=current_user.id)\
        .order_by(Job.created_at.desc()).limit(5).all()
    
    return render_template("hr/dashboard.html", stats=stats, recent_jobs=recent_jobs)


# ==================== JOB OPENINGS ====================
@hr_jobs_bp.route("/jobs")
@login_required
@role_required("admin", "hr")
def list_jobs():
    """List HR's job openings"""
    jobs = Job.query.filter_by(created_by=current_user.id)\
        .order_by(Job.created_at.desc()).all()
    return render_template("hr/jobs_list.html", jobs=jobs)


@hr_jobs_bp.route("/jobs/create", methods=["GET", "POST"])
@login_required
@role_required("hr")
def create_job():
    """Create new job opening"""
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        dept = request.form.get("department", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()
        
        if not title:
            flash("Job title is required", "danger")
            return redirect(url_for("hr_dashboard.create_job"))
        
        job = Job(
            title=title,
            dept=dept,
            location=location,
            description=description,
            status="open",
            created_by=current_user.id
        )
        db.session.add(job)
        db.session.commit()
        
        log_hr_action("create", "job", job.id, current_user.id, {"title": title})
        flash("Job opening created successfully", "success")
        return redirect(url_for("hr_dashboard.list_jobs"))
    
    return render_template("hr/job_edit.html", job=None)


@hr_jobs_bp.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("hr")
def edit_job(job_id):
    """Edit job opening"""
    job = Job.query.get_or_404(job_id)
    
    # Check authorization
    if job.created_by != current_user.id:
        flash("You don't have permission to edit this job", "danger")
        return redirect(url_for("hr_dashboard.list_jobs"))
    
    if request.method == "POST":
        job.title = request.form.get("title", job.title)
        job.dept = request.form.get("department", job.dept)
        job.location = request.form.get("location", job.location)
        job.description = request.form.get("description", job.description)
        job.status = request.form.get("status", job.status)
        db.session.commit()
        
        log_hr_action("update", "job", job.id, current_user.id)
        flash("Job opening updated successfully", "success")
        return redirect(url_for("hr_dashboard.list_jobs"))
    
    return render_template("hr/job_edit.html", job=job)


# ==================== INTERVIEW PLANS ====================
@hr_jobs_bp.route("/interview-plans")
@login_required
@role_required("admin", "hr")
def list_interview_plans():
    """List interview plans"""
    plans = InterviewPlan.query.all()
    return render_template("hr/interview_plans_list.html", plans=plans)


@hr_jobs_bp.route("/interview-plans/create", methods=["GET", "POST"])
@login_required
@role_required("admin", "hr")
def create_interview_plan():
    """Create new interview plan for a job"""
    if request.method == "POST":
        job_id = request.form.get("job_id", type=int)
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        
        if not job_id or not name:
            flash("Job and Plan name are required", "danger")
            return redirect(url_for("hr_dashboard.create_interview_plan"))
        
        plan = InterviewPlan(
            job_id=job_id,
            name=name,
            description=description,
            status="draft",
            created_by=current_user.id
        )
        db.session.add(plan)
        db.session.commit()
        
        log_hr_action("create", "interview_plan", plan.id, current_user.id, {"name": name})
        flash("Interview Plan created successfully", "success")
        return redirect(url_for("hr_dashboard.edit_interview_plan", plan_id=plan.id))
    
    # Get jobs created by this HR
    jobs = Job.query.filter_by(created_by=current_user.id).all()
    return render_template("hr/interview_plan_edit.html", plan=None, jobs=jobs)


@hr_jobs_bp.route("/interview-plans/<int:plan_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("hr")
def edit_interview_plan(plan_id):
    """Edit interview plan and configure rounds"""
    plan = InterviewPlan.query.get_or_404(plan_id)
    
    if request.method == "POST":
        plan.name = request.form.get("name", plan.name)
        plan.description = request.form.get("description", plan.description)
        plan.status = request.form.get("status", plan.status)
        db.session.commit()
        
        log_hr_action("update", "interview_plan", plan.id, current_user.id)
        flash("Interview Plan updated successfully", "success")
        return redirect(url_for("hr_dashboard.list_interview_plans"))
    
    jobs = Job.query.all()
    round_templates = RoundTemplate.query.filter_by(enabled=True).all()
    languages = ProgrammingLanguage.query.filter_by(enabled=True).all()
    
    return render_template("hr/interview_plan_edit.html", 
                          plan=plan, 
                          jobs=jobs,
                          round_templates=round_templates,
                          languages=languages)


# ==================== CANDIDATE INVITATIONS & SCHEDULING ====================
@hr_jobs_bp.route("/candidates")
@login_required
@role_required("hr")
def list_candidates():
    """List candidates for job invitations"""
    candidates = Candidate.query.all()
    return render_template("hr/candidates_list.html", candidates=candidates)


@hr_jobs_bp.route("/interview-schedules")
@login_required
@role_required("hr")
def list_interview_schedules():
    """List interview schedules"""
    schedules = InterviewSchedule.query.all()
    return render_template("hr/interview_schedules_list.html", schedules=schedules)


@hr_jobs_bp.route("/interview-schedules/create", methods=["GET", "POST"])
@login_required
@role_required("hr")
def create_interview_schedule():
    """Invite candidate and create interview schedule"""
    if request.method == "POST":
        candidate_id = request.form.get("candidate_id", type=int)
        plan_id = request.form.get("plan_id", type=int)
        
        if not candidate_id or not plan_id:
            flash("Candidate and Interview Plan are required", "danger")
            return redirect(url_for("hr_dashboard.create_interview_schedule"))
        
        # Check if schedule already exists
        existing = InterviewSchedule.query.filter_by(
            candidate_id=candidate_id, 
            interview_plan_id=plan_id
        ).first()
        
        if existing:
            flash("This candidate is already scheduled for this plan", "warning")
            return redirect(url_for("hr_dashboard.create_interview_schedule"))
        
        schedule = InterviewSchedule(
            candidate_id=candidate_id,
            interview_plan_id=plan_id,
            status="invited"
        )
        db.session.add(schedule)
        db.session.commit()
        
        log_hr_action("create", "interview_schedule", schedule.id, current_user.id)
        flash("Interview schedule created successfully", "success")
        return redirect(url_for("hr_dashboard.list_interview_schedules"))
    
    candidates = Candidate.query.all()
    plans = InterviewPlan.query.filter_by(status="active").all()
    return render_template("hr/interview_schedule_edit.html", 
                          schedule=None, 
                          candidates=candidates, 
                          plans=plans)


@hr_jobs_bp.route("/interview-schedules/<int:schedule_id>/recommend", methods=["POST"])
@login_required
@role_required("hr")
def recommend_candidate(schedule_id):
    """HR recommends pass/fail for candidate"""
    schedule = InterviewSchedule.query.get_or_404(schedule_id)
    recommendation = request.form.get("recommendation", "")  # pass or fail
    notes = request.form.get("notes", "")
    
    if recommendation not in ["pass", "fail"]:
        flash("Invalid recommendation", "danger")
        return redirect(url_for("hr_dashboard.list_interview_schedules"))
    
    # Store recommendation in feedback_json
    feedback = json.loads(schedule.feedback_json or "{}")
    feedback["hr_recommendation"] = recommendation
    feedback["hr_notes"] = notes
    feedback["recommended_at"] = datetime.utcnow().isoformat()
    
    schedule.feedback_json = json.dumps(feedback)
    db.session.commit()
    
    log_hr_action("update", "interview_schedule", schedule.id, current_user.id, 
                 {"recommendation": recommendation})
    
    flash(f"Recommendation recorded: {recommendation.upper()}", "success")
    return redirect(url_for("hr_dashboard.list_interview_schedules"))


# ==================== STUB ROUTES FOR LEGACY TEMPLATES ====================
@hr_jobs_bp.route("/candidates_list")
@login_required
@role_required("hr")
def candidates_list():
    """Legacy candidates list - redirect to main list"""
    return redirect(url_for("hr_jobs.list_candidates"))


@hr_jobs_bp.route("/analytics")
@login_required
@role_required("hr")
def analytics():
    """Legacy analytics view"""
    return render_template("dashboard/analytics.html")


@hr_jobs_bp.route("/reports")
@login_required
@role_required("hr")
def reports():
    """Legacy reports view"""
    return render_template("dashboard/reports.html")


@hr_jobs_bp.route("/export_candidates")
@login_required
@role_required("hr")
def export_candidates():
    """Export candidates data"""
    flash("Export feature coming soon", "info")
    return redirect(url_for("hr_jobs.list_candidates"))


@hr_jobs_bp.route("/export_analytics")
@login_required
@role_required("hr")
def export_analytics():
    """Export analytics data"""
    flash("Export feature coming soon", "info")
    return redirect(url_for("hr_jobs.analytics"))


@hr_jobs_bp.route("/export_funnel")
@login_required
@role_required("hr")
def export_funnel():
    """Export funnel data"""
    flash("Export feature coming soon", "info")
    return redirect(url_for("hr_jobs.analytics"))


@hr_jobs_bp.route("/export_skills")
@login_required
@role_required("hr")
def export_skills():
    """Export skills data"""
    flash("Export feature coming soon", "info")
    return redirect(url_for("hr_jobs.analytics"))


@hr_jobs_bp.route("/export_jobs")
@login_required
@role_required("hr")
def export_jobs():
    """Export jobs data"""
    flash("Export feature coming soon", "info")
    return redirect(url_for("hr_jobs.list_jobs"))


# ==================== HELPER FUNCTIONS ====================
def log_hr_action(action, entity_type, entity_id, user_id, payload=None):
    """Log HR action to audit log"""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        payload_json=json.dumps(payload) if payload else None
    )
    db.session.add(log)
    db.session.commit()

