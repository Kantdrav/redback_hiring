"""
HR Dashboard Routes - Dashboard, analytics, exports, and reports
"""
from flask import Blueprint, render_template, request, send_file, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from utils.rbac import role_required
from services.hr_analytics import HRAnalytics
from services.csv_exporter import CSVExporter
from models import db, Candidate, Job
from io import BytesIO
from datetime import datetime

hr_dashboard_bp = Blueprint("hr_dashboard", __name__, template_folder="../templates/dashboard")

@hr_dashboard_bp.route("/")
@login_required
@role_required("admin", "hr")
def dashboard():
    """Main HR dashboard"""
    metrics = HRAnalytics.get_dashboard_metrics()
    recent = HRAnalytics.get_recent_activity(days=7)
    top_candidates = HRAnalytics.get_top_candidates(limit=5)
    
    return render_template(
        "dashboard/index.html",
        metrics=metrics,
        recent_activity=recent,
        top_candidates=top_candidates
    )

@hr_dashboard_bp.route("/candidates")
@login_required
@role_required("admin", "hr")
def candidates_list():
    """Candidate list with filtering"""
    page = request.args.get("page", 1, type=int)
    job_id = request.args.get("job_id", None, type=int)
    status = request.args.get("status", None, type=str)
    min_score = request.args.get("min_score", None, type=int)
    search = request.args.get("search", "", type=str)
    
    # Get all jobs for filter dropdown
    jobs = Job.query.all()
    
    # Get filtered candidates
    result = HRAnalytics.get_candidates_with_filters(
        job_id=job_id,
        status=status,
        min_match_score=min_score,
        search_query=search if search else None,
        page=page,
        per_page=20
    )
    
    return render_template(
        "dashboard/candidates.html",
        candidates=result["candidates"],
        total=result["total"],
        page=page,
        pages=result["pages"],
        has_next=result["has_next"],
        has_prev=result["has_prev"],
        jobs=jobs,
        filters={
            "job_id": job_id,
            "status": status,
            "min_score": min_score,
            "search": search
        }
    )

@hr_dashboard_bp.route("/analytics")
@login_required
@role_required("admin", "hr")
def analytics():
    """Analytics and reports"""
    metrics = HRAnalytics.get_dashboard_metrics()
    skill_demand = HRAnalytics.get_skill_demand_analysis()
    funnel = HRAnalytics.get_hiring_funnel()
    match_dist = HRAnalytics.get_match_score_distribution()
    job_summary = HRAnalytics.get_job_candidate_summary()
    
    return render_template(
        "dashboard/analytics.html",
        metrics=metrics,
        skill_demand=skill_demand,
        funnel=funnel,
        match_distribution=match_dist,
        job_summary=job_summary
    )

@hr_dashboard_bp.route("/export/candidates")
@login_required
@role_required("admin", "hr")
def export_candidates():
    """Export candidates to CSV"""
    job_id = request.args.get("job_id", None, type=int)
    
    csv_data = CSVExporter.export_candidates_csv(job_id=job_id)
    
    # Create file response
    output = BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    filename = CSVExporter.generate_filename("candidates")
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@hr_dashboard_bp.route("/export/jobs")
@login_required
@role_required("admin", "hr")
def export_jobs():
    """Export jobs to CSV"""
    csv_data = CSVExporter.export_jobs_csv()
    
    output = BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    filename = CSVExporter.generate_filename("jobs")
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@hr_dashboard_bp.route("/export/analytics")
@login_required
@role_required("admin", "hr")
def export_analytics():
    """Export analytics summary to CSV"""
    metrics = HRAnalytics.get_dashboard_metrics()
    csv_data = CSVExporter.export_analytics_csv(metrics)
    
    output = BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    filename = CSVExporter.generate_filename("analytics")
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@hr_dashboard_bp.route("/export/skills")
@login_required
@role_required("admin", "hr")
def export_skills():
    """Export skill demand analysis to CSV"""
    skill_data = HRAnalytics.get_skill_demand_analysis()
    csv_data = CSVExporter.export_skill_demand_csv(skill_data)
    
    output = BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    filename = CSVExporter.generate_filename("skill_demand")
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@hr_dashboard_bp.route("/export/funnel")
@login_required
@role_required("admin", "hr")
def export_funnel():
    """Export hiring funnel to CSV"""
    funnel = HRAnalytics.get_hiring_funnel()
    csv_data = CSVExporter.export_hiring_funnel_csv(funnel)
    
    output = BytesIO()
    output.write(csv_data.encode('utf-8'))
    output.seek(0)
    
    filename = CSVExporter.generate_filename("hiring_funnel")
    
    return send_file(
        output,
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

@hr_dashboard_bp.route("/candidate/<int:candidate_id>/update-status", methods=["POST"])
@login_required
@role_required("admin", "hr")
def update_candidate_status(candidate_id):
    """Update candidate status"""
    candidate = Candidate.query.get_or_404(candidate_id)
    new_status = request.form.get("status")
    
    if new_status in ["applied", "screening", "interview", "offer", "hired", "rejected"]:
        candidate.status = new_status
        db.session.commit()
        flash(f"Candidate status updated to {new_status}", "success")
    else:
        flash("Invalid status", "danger")
    
    return redirect(request.referrer or url_for("hr_dashboard.candidates_list"))

@hr_dashboard_bp.route("/api/metrics")
@login_required
@role_required("admin", "hr")
def api_metrics():
    """API endpoint for metrics (for charts/dashboards)"""
    metrics = HRAnalytics.get_dashboard_metrics()
    return jsonify(metrics)

@hr_dashboard_bp.route("/api/funnel")
@login_required
@role_required("admin", "hr")
def api_funnel():
    """API endpoint for hiring funnel"""
    funnel = HRAnalytics.get_hiring_funnel()
    return jsonify(funnel)

@hr_dashboard_bp.route("/api/skills")
@login_required
@role_required("admin", "hr")
def api_skills():
    """API endpoint for skill demand"""
    skills = HRAnalytics.get_skill_demand_analysis()
    return jsonify({
        "skills": [{"skill": s[0], "count": s[1]} for s in skills]
    })

@hr_dashboard_bp.route("/reports")
@login_required
@role_required("admin", "hr")
def reports():
    """Reports page"""
    metrics = HRAnalytics.get_dashboard_metrics()
    
    return render_template(
        "dashboard/reports.html",
        metrics=metrics
    )
