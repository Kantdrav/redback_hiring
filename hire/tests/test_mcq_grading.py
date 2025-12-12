import pytest
from services.mcq_engine import grade_mcq
from models.mcq_question import MCQQuestion
from models import db
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        # create sample question
        q = MCQQuestion(round_id=1, question_text="Q1", choices_json='["a","b","c"]', correct_index=1, marks=2.0)
        db.session.add(q); db.session.commit()
        yield app.test_client()
        db.drop_all()

def test_grade_mcq_basic(client):
    # find question id
    from models.mcq_question import MCQQuestion
    q = MCQQuestion.query.first()
    ans = { str(q.id): 1 }  # correct answer
    res = grade_mcq(1, ans)
    assert res["obtained_marks"] == 2.0
    assert res["total_marks"] == 2.0
