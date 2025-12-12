from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*roles):
    """
    Decorator to require one of the given roles.
    Usage: @role_required('admin','hr')
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user or not getattr(current_user, "is_authenticated", False):
                abort(401)
            user_role = getattr(current_user, "role", None)
            if user_role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator

def roles_allowed(*roles):
    # alias
    return role_required(*roles)
