import pytest
from app import create_app
from models import db
from models.user import User
from models.candidate import Candidate
from models.round import Round
from models.interview import Interview
from datetime import datetime, timedelta

@pytest.fixture
def app_client():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # create user interviewer
        u = User(email="int@example.com", name="Interviewer", role="interviewer")
        u.set_password("pass")
        db.session.add(u)
        # candidate
        c = Candidate(name="Cand", email="cand@example.com")
        db.session.add(c)
        r = Round(name="Tech", type="technical")
        db.session.add(r)
        db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_schedule_insertion(app_client):
    from models.interview import Interview
    # schedule an interview
    iv = Interview(round_id=1, candidate_id=1, interviewer_id=1, scheduled_at_utc=datetime.utcnow()+timedelta(days=1))
    db.session.add(iv); db.session.commit()
    assert Interview.query.count() == 1
