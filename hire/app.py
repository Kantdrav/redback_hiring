from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db
from auth import auth_blueprint, login_manager
from views_jobs import jobs_bp
from rag_resume import rag_bp
from routes.admin_users import admin_users_bp
from routes.admin_dashboard import admin_dashboard_bp
from routes.interviews import interviews_bp
from routes.hr_jobs import hr_jobs_bp
from routes.interviewer import interviewer_bp
from routes.candidate import candidate_bp

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
