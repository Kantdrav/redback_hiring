from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import db, User, UserImpersonation, Job, Candidate, Interview, Round
from datetime import datetime
import json

admin_users_bp = Blueprint("admin_users", __name__, template_folder="../templates/admin")

@admin_users_bp.route("/users")
@login_required
@role_required("admin")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users_list.html", users=users)

@admin_users_bp.route("/users/create", methods=["GET","POST"])
@login_required
@role_required("admin")
def create_user():
    if request.method == "POST":
        email = request.form.get("email").lower()
        name = request.form.get("name")
        role = request.form.get("role","candidate")
        password = request.form.get("password")
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "warning")
            return redirect(url_for("admin_users.create_user"))
        u = User(email=email, name=name, role=role)
        u.set_password(password)
        db.session.add(u); db.session.commit()
        flash("User created", "success")
        return redirect(url_for("admin_users.list_users"))
    return render_template("admin/users_edit.html", user=None)

@admin_users_bp.route("/users/<int:user_id>/edit", methods=["GET","POST"])
@login_required
@role_required("admin")
def edit_user(user_id):
    u = User.query.get_or_404(user_id)
    if request.method == "POST":
        u.name = request.form.get("name")
        u.role = request.form.get("role")
        pw = request.form.get("password")
        if pw:
            u.set_password(pw)
        db.session.commit()
        flash("User updated", "success")
        return redirect(url_for("admin_users.list_users"))
    return render_template("admin/users_edit.html", user=u)

@admin_users_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@login_required
@role_required("admin")
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    flash("User deleted", "info")
    return redirect(url_for("admin_users.list_users"))


# ===== ADMIN IMPERSONATION ACTIONS =====

@admin_users_bp.route("/users/<int:user_id>/impersonate-apply", methods=["POST"])
@login_required
@role_required("admin")
def impersonate_apply_job(user_id):
    """Admin applies job on behalf of a user (candidate)"""
    try:
        target_user = User.query.get_or_404(user_id)
        job_id = request.form.get("job_id")
        
        if not job_id:
            flash("Job not selected", "danger")
            return redirect(url_for("admin_users.list_users"))
        
        job = Job.query.get_or_404(job_id)
        
        # Check if candidate already applied
        candidate = Candidate.query.filter_by(user_id=target_user.id).first()
        if not candidate:
            candidate = Candidate(user_id=target_user.id, email=target_user.email, name=target_user.name)
            db.session.add(candidate)
            db.session.flush()
        
        # Check if already applied
        if candidate.id in [c.id for c in job.candidates]:
            flash(f"User already applied for {job.title}", "warning")
            impersonation = UserImpersonation(
                admin_id=current_user.id,
                target_user_id=target_user.id,
                action="apply_job",
                details_json=json.dumps({"job_id": job_id, "job_title": job.title}),
                status="skipped",
                error_message="User already applied for this job"
            )
        else:
            job.candidates.append(candidate)
            db.session.commit()
            flash(f"Applied {target_user.name} to {job.title}", "success")
            
            impersonation = UserImpersonation(
                admin_id=current_user.id,
                target_user_id=target_user.id,
                action="apply_job",
                details_json=json.dumps({"job_id": job_id, "job_title": job.title}),
                status="success"
            )
        
        db.session.add(impersonation)
        db.session.commit()
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        impersonation = UserImpersonation(
            admin_id=current_user.id,
            target_user_id=user_id,
            action="apply_job",
            status="failed",
            error_message=str(e)
        )
        db.session.add(impersonation)
        db.session.commit()
    
    return redirect(url_for("admin_users.user_detail", user_id=user_id))


@admin_users_bp.route("/users/<int:user_id>/impersonate-assign-interview", methods=["POST"])
@login_required
@role_required("admin")
def impersonate_assign_interview(user_id):
    """Admin assigns interview/quiz to a candidate on their behalf"""
    try:
        target_user = User.query.get_or_404(user_id)
        round_id = request.form.get("round_id")
        
        if not round_id:
            flash("Round/Quiz not selected", "danger")
            return redirect(url_for("admin_users.list_users"))
        
        round_obj = Round.query.get_or_404(round_id)
        
        # Get or create candidate
        candidate = Candidate.query.filter_by(user_id=target_user.id).first()
        if not candidate:
            candidate = Candidate(user_id=target_user.id, email=target_user.email, name=target_user.name)
            db.session.add(candidate)
            db.session.flush()
        
        # Get admin user as interviewer
        admin_user = current_user
        
        # Check if interview already exists
        existing = Interview.query.filter_by(
            candidate_id=candidate.id,
            round_id=round_id
        ).first()
        
        if existing:
            flash(f"Interview already assigned for {round_obj.name}", "warning")
            impersonation = UserImpersonation(
                admin_id=current_user.id,
                target_user_id=target_user.id,
                action="assign_interview",
                details_json=json.dumps({"round_id": round_id, "round_name": round_obj.name}),
                status="skipped",
                error_message="Interview already assigned"
            )
        else:
            interview = Interview(
                candidate_id=candidate.id,
                round_id=round_id,
                interviewer_id=admin_user.id,
                status="scheduled"
            )
            db.session.add(interview)
            db.session.commit()
            flash(f"Assigned {round_obj.name} to {target_user.name}", "success")
            
            impersonation = UserImpersonation(
                admin_id=current_user.id,
                target_user_id=target_user.id,
                action="assign_interview",
                details_json=json.dumps({"round_id": round_id, "round_name": round_obj.name}),
                status="success"
            )
        
        db.session.add(impersonation)
        db.session.commit()
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        impersonation = UserImpersonation(
            admin_id=current_user.id,
            target_user_id=user_id,
            action="assign_interview",
            status="failed",
            error_message=str(e)
        )
        db.session.add(impersonation)
        db.session.commit()
    
    return redirect(url_for("admin_users.user_detail", user_id=user_id))


@admin_users_bp.route("/users/<int:user_id>/impersonate-update-experience", methods=["POST"])
@login_required
@role_required("admin")
def impersonate_update_experience(user_id):
    """Admin updates candidate experience level"""
    try:
        target_user = User.query.get_or_404(user_id)
        experience_years = float(request.form.get("experience_years", 0))
        
        candidate = Candidate.query.filter_by(user_id=target_user.id).first()
        if not candidate:
            candidate = Candidate(user_id=target_user.id, email=target_user.email, name=target_user.name)
            db.session.add(candidate)
            db.session.flush()
        
        candidate.experience_years = experience_years
        db.session.commit()
        flash(f"Updated {target_user.name} experience to {experience_years} years", "success")
        
        impersonation = UserImpersonation(
            admin_id=current_user.id,
            target_user_id=target_user.id,
            action="update_experience",
            details_json=json.dumps({"experience_years": experience_years}),
            status="success"
        )
        db.session.add(impersonation)
        db.session.commit()
        
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        impersonation = UserImpersonation(
            admin_id=current_user.id,
            target_user_id=user_id,
            action="update_experience",
            status="failed",
            error_message=str(e)
        )
        db.session.add(impersonation)
        db.session.commit()
    
    return redirect(url_for("admin_users.user_detail", user_id=user_id))


@admin_users_bp.route("/users/<int:user_id>")
@login_required
@role_required("admin")
def user_detail(user_id):
    """Display user details with impersonation action options"""
    user = User.query.get_or_404(user_id)
    jobs = Job.query.filter_by(status="active").all() if user.role == "candidate" else []
    rounds = Round.query.all() if user.role == "candidate" else []
    candidate = Candidate.query.filter_by(user_id=user_id).first()
    impersonation_logs = UserImpersonation.query.filter_by(target_user_id=user_id).order_by(
        UserImpersonation.created_at.desc()
    ).limit(20).all()
    
    return render_template(
        "admin/user_detail.html",
        user=user,
        candidate=candidate,
        jobs=jobs,
        rounds=rounds,
        impersonation_logs=impersonation_logs
    )
