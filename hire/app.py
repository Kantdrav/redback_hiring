from flask import Flask, render_template, redirect, url_for, request
from config import Config
from models import db, WebsiteVisit
from auth import auth_blueprint, login_manager
from views_jobs import jobs_bp
from rag_resume import rag_bp
from routes.admin_users import admin_users_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.interviews import interviews_bp
from routes.hr_jobs import hr_jobs_bp
from routes.interviewer import interviewer_bp
from routes.candidate import candidate_bp
from datetime import datetime
from flask_login import current_user
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(auth_blueprint)
    
    # Admin routes
    app.register_blueprint(admin_users_bp, url_prefix="/admin")
    app.register_blueprint(admin_dashboard_bp, url_prefix="/admin")
    
    # HR routes
    app.register_blueprint(hr_jobs_bp, url_prefix="/hr")
    
    # Interviewer routes
    app.register_blueprint(interviewer_bp, url_prefix="/interviewer")
    
    # Candidate routes
    app.register_blueprint(candidate_bp, url_prefix="/candidate")
    
    # Legacy routes
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(interviews_bp, url_prefix="/interviews")
    app.register_blueprint(rag_bp, url_prefix="/rag")

    # ===== WEBSITE VISIT TRACKING =====
    @app.before_request
    def track_visit():
        """Track website visits before processing request"""
        try:
            start_time = time.time()
            
            # Skip tracking for static files
            if request.path.startswith('/static/'):
                return
            
            # Store start time for response time calculation
            request._start_time = start_time
        except Exception as e:
            print(f"Error in before_request: {e}")

    @app.after_request
    def log_visit(response):
        """Log website visit after request"""
        try:
            # Skip tracking for static files
            if request.path.startswith('/static/'):
                return response
            
            # Calculate response time
            start_time = getattr(request, '_start_time', time.time())
            response_time_ms = (time.time() - start_time) * 1000
            
            # Get visitor info
            user_id = current_user.id if current_user.is_authenticated else None
            ip_address = request.remote_addr or 'unknown'
            user_agent = request.user_agent.string[:500] if request.user_agent else 'unknown'
            
            # Log visit (avoid logging analytics page to prevent infinite logging)
            if not request.path.startswith('/admin/analytics') and not request.path.startswith('/admin/impersonation-logs'):
                visit = WebsiteVisit(
                    user_id=user_id,
                    ip_address=ip_address,
                    user_agent=user_agent,
                    endpoint=request.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=response_time_ms,
                    visited_at=datetime.utcnow()
                )
                db.session.add(visit)
                db.session.commit()
        except Exception as e:
            print(f"Error in after_request: {e}")
        
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/admin")
    def admin_dashboard():
        return redirect(url_for("admin_users.list_users"))

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
