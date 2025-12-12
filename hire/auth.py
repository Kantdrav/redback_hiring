from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from models import db, User

auth_blueprint = Blueprint("auth", __name__, template_folder="templates/auth")
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# Admin bypass token - set this to allow admin access without login
ADMIN_BYPASS_TOKEN = "admin-access-token-2025"

# We create a small adapter to integrate SQLAlchemy User with Flask-Login
class UserLogin(UserMixin):
    def __init__(self, user):
        self.user = user

    @property
    def id(self):
        return str(self.user.id)

    def get_attr(self, name):
        return getattr(self.user, name, None)
    
    @property
    def role(self):
        return getattr(self.user, 'role', 'candidate')
    
    @property
    def email(self):
        return getattr(self.user, 'email', None)
    
    @property
    def name(self):
        return getattr(self.user, 'name', None)

@login_manager.user_loader
def load_user(user_id):
    u = User.query.get(int(user_id))
    if u:
        return UserLogin(u)
    return None

# register login manager in app factory
def init_app(app):
    login_manager.init_app(app)

@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]
        name = request.form.get("name")
        role = request.form.get("role", "candidate")
        
        # Restrict HR role - only admin can create HR users
        if role == "hr":
            flash("HR accounts must be created by an administrator. Please contact your admin.", "warning")
            return redirect(url_for("auth.register"))
        
        # Only allow candidate and interviewer self-registration
        if role not in ["candidate", "interviewer"]:
            role = "candidate"
        
        if User.query.filter_by(email=email).first():
            flash("Email exists", "warning")
            return redirect(url_for("auth.register"))
        
        u = User(email=email, name=name, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        flash(f"Registered as {role.capitalize()}. Please login.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html")

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].lower()
        pw = request.form["password"]
        selected_role = request.form.get("role", "")
        admin_token = request.form.get("admin_token", "")
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(pw):
            flash("Invalid credentials", "danger")
            return redirect(url_for("auth.login"))
        
        # Validate role matches
        if selected_role and user.role != selected_role:
            flash(f"Invalid role selected. Your account role is: {user.role.capitalize()}", "warning")
            return redirect(url_for("auth.login"))
        
        # Admin login requires token verification
        if user.role == "admin":
            if admin_token != ADMIN_BYPASS_TOKEN:
                flash("Admin login requires valid admin token", "danger")
                return redirect(url_for("auth.login"))
        
        login_user(UserLogin(user))
        flash(f"Logged in as {user.role.capitalize()}", "success")
        
        # Redirect admin to admin panel
        if user.role == "admin":
            return redirect("/admin")
        return redirect("/")
    return render_template("auth/login.html")

@auth_blueprint.route("/admin_access", methods=["POST"])
def admin_access():
    """Admin access without password - requires valid bypass token"""
    token = request.form.get("token", "")
    if token == ADMIN_BYPASS_TOKEN:
        # Get or create admin user
        admin = User.query.filter_by(email="admin@redback.local").first()
        if not admin:
            admin = User(
                email="admin@redback.local",
                name="Administrator",
                role="admin"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
        
        login_user(UserLogin(admin))
        flash("Admin access granted", "success")
        return redirect("/admin")
    else:
        flash("Invalid admin token", "danger")
        return redirect(url_for("auth.login"))

@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(url_for("auth.login"))
