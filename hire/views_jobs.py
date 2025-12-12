from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Job
from flask_login import current_user, login_required

jobs_bp = Blueprint("jobs", __name__, template_folder="templates/jobs")

@jobs_bp.route("/")
@login_required
def list_jobs():
    jobs = Job.query.all()
    return render_template("jobs/list.html", jobs=jobs)

@jobs_bp.route("/<int:job_id>")
@login_required
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template("jobs/view.html", job=job)

@jobs_bp.route("/<int:job_id>/edit", methods=["GET", "POST"])
@login_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    
    if request.method == "POST":
        job.title = request.form.get("title", job.title)
        job.dept = request.form.get("dept", job.dept)
        job.location = request.form.get("location", job.location)
        job.description = request.form.get("description", job.description)
        job.status = request.form.get("status", job.status)
        db.session.commit()
        flash("Job updated", "success")
        return redirect(url_for("jobs.view_job", job_id=job.id))
    
    return render_template("jobs/edit.html", job=job)

@jobs_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_job():
    if request.method == "POST":
        title = request.form["title"]
        dept = request.form.get("dept")
        loc = request.form.get("location")
        desc = request.form.get("description")
        job = Job(title=title, dept=dept, location=loc, description=desc, created_by=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash("Job created", "success")
        return redirect(url_for("jobs.list_jobs"))
    return render_template("jobs/create.html")

