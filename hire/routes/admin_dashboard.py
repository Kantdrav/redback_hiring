"""Admin Dashboard - Manage users, roles, scoring policies, question banks, round templates"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import (
    db, User, ProgrammingLanguage, QuestionBank, QuestionBankItem, 
    ScoringPolicy, RoundTemplate, AuditLog, WebsiteVisit, UserImpersonation
)
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import json

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, template_folder="../templates/admin")


# ==================== ADMIN DASHBOARD MAIN ====================
@admin_dashboard_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    """Main admin dashboard with overview stats"""
    stats = {
        "total_users": User.query.count(),
        "total_languages": ProgrammingLanguage.query.count(),
        "total_question_banks": QuestionBank.query.count(),
        "total_scoring_policies": ScoringPolicy.query.count(),
        "website_visits_today": WebsiteVisit.query.filter(
            WebsiteVisit.visited_at >= datetime.utcnow().date()
        ).count(),
        "total_website_visits": WebsiteVisit.query.count(),
        "impersonation_actions_today": UserImpersonation.query.filter(
            UserImpersonation.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count(),
    }
    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html", stats=stats, recent_logs=recent_logs)


# ===== WEBSITE VISIT ANALYTICS =====
@admin_dashboard_bp.route("/analytics")
@login_required
@role_required("admin")
def analytics():
    """Display website visit analytics and metrics"""
    page = request.args.get("page", 1, type=int)
    per_page = 50
    
    # Get visit statistics
    total_visits = WebsiteVisit.query.count()
    unique_visitors = db.session.query(func.count(func.distinct(WebsiteVisit.user_id))).scalar()
    unique_ips = db.session.query(func.count(func.distinct(WebsiteVisit.ip_address))).scalar()
    
    # Visits today
    today_visits = WebsiteVisit.query.filter(
        WebsiteVisit.visited_at >= datetime.utcnow().date()
    ).count()
    
    # Most visited endpoints
    top_endpoints = db.session.query(
        WebsiteVisit.endpoint,
        func.count(WebsiteVisit.id).label('visit_count')
    ).group_by(WebsiteVisit.endpoint).order_by(
        desc('visit_count')
    ).limit(10).all()
    
    # Most active users
    top_users = db.session.query(
        User,
        func.count(WebsiteVisit.id).label('visit_count')
    ).join(WebsiteVisit, WebsiteVisit.user_id == User.id).group_by(
        User.id
    ).order_by(desc('visit_count')).limit(10).all()
    
    # Recent visits with pagination
    recent_visits = WebsiteVisit.query.order_by(
        WebsiteVisit.visited_at.desc()
    ).paginate(page=page, per_page=per_page)
    
    # Hourly visit count (last 24 hours)
    hourly_visits = {}
    for i in range(24):
        hour_start = datetime.utcnow().replace(hour=i, minute=0, second=0, microsecond=0)
        hour_end = hour_start + timedelta(hours=1)
        count = WebsiteVisit.query.filter(
            WebsiteVisit.visited_at >= hour_start,
            WebsiteVisit.visited_at < hour_end
        ).count()
        hourly_visits[i] = count
    
    stats = {
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "unique_ips": unique_ips,
        "today_visits": today_visits,
    }
    
    return render_template(
        "admin/analytics.html",
        stats=stats,
        recent_visits=recent_visits,
        top_endpoints=top_endpoints,
        top_users=top_users,
        hourly_visits=hourly_visits
    )


# ===== IMPERSONATION AUDIT LOG =====
@admin_dashboard_bp.route("/impersonation-logs")
@login_required
@role_required("admin")
def impersonation_logs():
    """Display admin impersonation action logs"""
    page = request.args.get("page", 1, type=int)
    action_filter = request.args.get("action", None)
    per_page = 50
    
    query = UserImpersonation.query.order_by(UserImpersonation.created_at.desc())
    
    if action_filter:
        query = query.filter_by(action=action_filter)
    
    logs = query.paginate(page=page, per_page=per_page)
    
    # Get action statistics
    action_stats = db.session.query(
        UserImpersonation.action,
        func.count(UserImpersonation.id).label('count'),
        func.sum(func.cast(UserImpersonation.status == 'success', db.Integer)).label('success_count')
    ).group_by(UserImpersonation.action).all()
    
    stats = {
        "total_actions": UserImpersonation.query.count(),
        "today_actions": UserImpersonation.query.filter(
            UserImpersonation.created_at >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count(),
        "successful_actions": UserImpersonation.query.filter_by(status="success").count(),
        "failed_actions": UserImpersonation.query.filter_by(status="failed").count(),
    }
    
    return render_template(
        "admin/impersonation_logs.html",
        logs=logs,
        action_stats=action_stats,
        stats=stats,
        action_filter=action_filter
    )


# ==================== PROGRAMMING LANGUAGES ====================
@admin_dashboard_bp.route("/languages")
@login_required
@role_required("admin")
def list_languages():
    """List all programming languages"""
    languages = ProgrammingLanguage.query.all()
    return render_template("admin/languages_list.html", languages=languages)


@admin_dashboard_bp.route("/languages/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_language():
    """Add new programming language"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Language name is required", "danger")
            return redirect(url_for("admin_dashboard.add_language"))
        
        if ProgrammingLanguage.query.filter_by(name=name).first():
            flash(f"Language '{name}' already exists", "warning")
            return redirect(url_for("admin_dashboard.add_language"))
        
        lang = ProgrammingLanguage(name=name, enabled=True)
        db.session.add(lang)
        db.session.commit()
        
        # Log action
        log_admin_action("create", "programming_language", lang.id, current_user.id, {"name": name})
        flash(f"Language '{name}' added successfully", "success")
        return redirect(url_for("admin_dashboard.list_languages"))
    
    return render_template("admin/language_edit.html", language=None)


@admin_dashboard_bp.route("/languages/<int:lang_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_language(lang_id):
    """Edit programming language"""
    lang = ProgrammingLanguage.query.get_or_404(lang_id)
    
    if request.method == "POST":
        lang.name = request.form.get("name", lang.name)
        lang.enabled = request.form.get("enabled") == "on"
        db.session.commit()
        
        log_admin_action("update", "programming_language", lang.id, current_user.id, {"name": lang.name})
        flash("Language updated successfully", "success")
        return redirect(url_for("admin_dashboard.list_languages"))
    
    return render_template("admin/language_edit.html", language=lang)


# ==================== QUESTION BANKS ====================
@admin_dashboard_bp.route("/question-banks")
@login_required
@role_required("admin")
def list_question_banks():
    """List all question banks"""
    language_id = request.args.get("language", type=int)
    query = QuestionBank.query
    
    if language_id:
        query = query.filter_by(language_id=language_id)
    
    banks = query.order_by(QuestionBank.created_at.desc()).all()
    languages = ProgrammingLanguage.query.filter_by(enabled=True).all()
    
    return render_template("admin/question_banks_list.html", 
                          question_banks=banks, 
                          languages=languages,
                          selected_language=language_id)


@admin_dashboard_bp.route("/question-banks/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_question_bank():
    """Create new question bank"""
    if request.method == "POST":
        language_id = request.form.get("language_id", type=int)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        
        if not language_id or not title:
            flash("Language and Title are required", "danger")
            return redirect(url_for("admin_dashboard.create_question_bank"))
        
        bank = QuestionBank(
            language_id=language_id,
            title=title,
            description=description,
            created_by=current_user.id,
            enabled=True
        )
        db.session.add(bank)
        db.session.commit()
        
        log_admin_action("create", "question_bank", bank.id, current_user.id, 
                        {"title": title, "language_id": language_id})
        
        flash("Question Bank created successfully", "success")
        return redirect(url_for("admin_dashboard.edit_question_bank", bank_id=bank.id))
    
    languages = ProgrammingLanguage.query.filter_by(enabled=True).all()
    return render_template("admin/question_bank_edit.html", bank=None, languages=languages)


@admin_dashboard_bp.route("/question-banks/<int:bank_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_question_bank(bank_id):
    """Edit question bank and manage questions"""
    bank = QuestionBank.query.get_or_404(bank_id)
    
    if request.method == "POST":
        bank.title = request.form.get("title", bank.title)
        bank.description = request.form.get("description", bank.description)
        bank.enabled = request.form.get("enabled") == "on"
        db.session.commit()
        
        log_admin_action("update", "question_bank", bank.id, current_user.id)
        flash("Question Bank updated successfully", "success")
        return redirect(url_for("admin_dashboard.list_question_banks"))
    
    languages = ProgrammingLanguage.query.filter_by(enabled=True).all()
    questions = QuestionBankItem.query.filter_by(bank_id=bank_id).all()
    
    return render_template("admin/question_bank_edit.html", 
                          bank=bank, 
                          languages=languages,
                          questions=questions)


@admin_dashboard_bp.route("/question-banks/<int:bank_id>/questions/add", methods=["GET", "POST"])
@login_required
@role_required("admin")
def add_question(bank_id):
    """Add question to bank"""
    bank = QuestionBank.query.get_or_404(bank_id)
    
    if request.method == "POST":
        question_text = request.form.get("question_text", "").strip()
        question_type = request.form.get("question_type", "mcq")
        difficulty = request.form.get("difficulty", "medium")
        time_limit = request.form.get("time_limit", 300, type=int)
        
        if not question_text:
            flash("Question text is required", "danger")
            return redirect(url_for("admin_dashboard.add_question", bank_id=bank_id))
        
        # Handle MCQ choices
        choices = []
        if question_type == "mcq":
            choices_input = request.form.get("choices", "").strip()
            correct_index = request.form.get("correct_index", 0, type=int)
            choices = [c.strip() for c in choices_input.split("\n") if c.strip()]
        
        question = QuestionBankItem(
            bank_id=bank_id,
            question_text=question_text,
            question_type=question_type,
            difficulty=difficulty,
            choices_json=json.dumps(choices) if choices else None,
            time_limit_seconds=time_limit,
            enabled=True
        )
        db.session.add(question)
        db.session.commit()
        
        log_admin_action("create", "question_bank_item", question.id, current_user.id)
        flash("Question added successfully", "success")
        return redirect(url_for("admin_dashboard.edit_question_bank", bank_id=bank_id))
    
    return render_template("admin/question_edit.html", bank=bank, question=None)


# ==================== SCORING POLICIES ====================
@admin_dashboard_bp.route("/scoring-policies")
@login_required
@role_required("admin")
def list_scoring_policies():
    """List all scoring policies"""
    policies = ScoringPolicy.query.order_by(ScoringPolicy.created_at.desc()).all()
    return render_template("admin/scoring_policies_list.html", policies=policies)


@admin_dashboard_bp.route("/scoring-policies/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_scoring_policy():
    """Create new scoring policy"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        passing_score = request.form.get("passing_score", 60, type=int)
        
        if not name:
            flash("Policy name is required", "danger")
            return redirect(url_for("admin_dashboard.create_scoring_policy"))
        
        policy_config = {
            "passing_score": passing_score,
            "weights": {
                "technical": request.form.get("weight_technical", 40, type=int),
                "coding": request.form.get("weight_coding", 30, type=int),
                "hr_round": request.form.get("weight_hr", 30, type=int)
            }
        }
        
        policy = ScoringPolicy(
            name=name,
            description=description,
            policy_json=json.dumps(policy_config),
            created_by=current_user.id,
            enabled=True
        )
        db.session.add(policy)
        db.session.commit()
        
        log_admin_action("create", "scoring_policy", policy.id, current_user.id, {"name": name})
        flash("Scoring Policy created successfully", "success")
        return redirect(url_for("admin_dashboard.list_scoring_policies"))
    
    return render_template("admin/scoring_policy_edit.html", policy=None)


@admin_dashboard_bp.route("/scoring-policies/<int:policy_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_scoring_policy(policy_id):
    """Edit scoring policy"""
    policy = ScoringPolicy.query.get_or_404(policy_id)
    
    if request.method == "POST":
        policy.name = request.form.get("name", policy.name)
        policy.description = request.form.get("description", policy.description)
        policy.enabled = request.form.get("enabled") == "on"
        
        policy_config = policy.get_policy()
        policy_config["passing_score"] = request.form.get("passing_score", 60, type=int)
        policy_config["weights"] = {
            "technical": request.form.get("weight_technical", 40, type=int),
            "coding": request.form.get("weight_coding", 30, type=int),
            "hr_round": request.form.get("weight_hr", 30, type=int)
        }
        policy.policy_json = json.dumps(policy_config)
        db.session.commit()
        
        log_admin_action("update", "scoring_policy", policy.id, current_user.id)
        flash("Scoring Policy updated successfully", "success")
        return redirect(url_for("admin_dashboard.list_scoring_policies"))
    
    return render_template("admin/scoring_policy_edit.html", policy=policy)


# ==================== ROUND TEMPLATES ====================
@admin_dashboard_bp.route("/round-templates")
@login_required
@role_required("admin")
def list_round_templates():
    """List all round templates"""
    templates = RoundTemplate.query.order_by(RoundTemplate.created_at.desc()).all()
    return render_template("admin/round_templates_list.html", templates=templates)


@admin_dashboard_bp.route("/round-templates/create", methods=["GET", "POST"])
@login_required
@role_required("admin")
def create_round_template():
    """Create new round template"""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        round_type = request.form.get("type", "").strip()
        description = request.form.get("description", "").strip()
        duration = request.form.get("duration", 30, type=int)
        
        if not name or not round_type:
            flash("Name and Type are required", "danger")
            return redirect(url_for("admin_dashboard.create_round_template"))
        
        template = RoundTemplate(
            name=name,
            type=round_type,
            description=description,
            duration_minutes=duration,
            created_by=current_user.id,
            enabled=True
        )
        db.session.add(template)
        db.session.commit()
        
        log_admin_action("create", "round_template", template.id, current_user.id, {"name": name})
        flash("Round Template created successfully", "success")
        return redirect(url_for("admin_dashboard.list_round_templates"))
    
    return render_template("admin/round_template_edit.html", template=None)


@admin_dashboard_bp.route("/round-templates/<int:template_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("admin")
def edit_round_template(template_id):
    """Edit round template"""
    template = RoundTemplate.query.get_or_404(template_id)
    
    if request.method == "POST":
        template.name = request.form.get("name", template.name)
        template.type = request.form.get("type", template.type)
        template.description = request.form.get("description", template.description)
        template.duration_minutes = request.form.get("duration", template.duration_minutes, type=int)
        template.enabled = request.form.get("enabled") == "on"
        db.session.commit()
        
        log_admin_action("update", "round_template", template.id, current_user.id)
        flash("Round Template updated successfully", "success")
        return redirect(url_for("admin_dashboard.list_round_templates"))
    
    return render_template("admin/round_template_edit.html", template=template)


# ==================== AUDIT LOGS ====================
@admin_dashboard_bp.route("/audit-logs")
@login_required
@role_required("admin")
def view_audit_logs():
    """View all audit logs"""
    page = request.args.get("page", 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=50)
    return render_template("admin/audit_logs.html", logs=logs)


# ==================== HELPER FUNCTIONS ====================
def log_admin_action(action, entity_type, entity_id, user_id, payload=None):
    """Log admin action to audit log"""
    log = AuditLog(
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        user_id=user_id,
        payload_json=json.dumps(payload) if payload else None
    )
    db.session.add(log)
    db.session.commit()
