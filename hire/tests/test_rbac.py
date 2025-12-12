import pytest
from utils.rbac import role_required
from types import SimpleNamespace
from flask import Flask
from flask_login import LoginManager, login_user

# Helper to fake a function with decorator
def test_role_required_decorator(monkeypatch):
    # create a fake user with role 'hr'
    fake_user = SimpleNamespace(is_authenticated=True, role="hr", id=1)
    # create a decorator output
    from flask import g

    app = Flask(__name__)
    lm = LoginManager()
    lm.init_app(app)
    with app.test_request_context():
        # monkeypatch current_user
        import utils.rbac as rbacmod
        monkeypatch.setattr(rbacmod, "current_user", fake_user)
        @role_required("admin","hr")
        def f(a,b):
            return "ok"
        assert f(1,2) == "ok"
        # now change role to candidate
        fake_user.role = "candidate"
        with pytest.raises(Exception):
            # decorator should abort with 403
            f(1,2)
