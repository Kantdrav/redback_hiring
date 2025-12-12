from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from utils.rbac import role_required
from models import db, User

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
