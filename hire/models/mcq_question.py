from datetime import datetime
import json
from .db import db

class MCQQuestion(db.Model):
    __tablename__ = "mcq_questions"
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"))
    question_text = db.Column(db.Text)
    choices_json = db.Column(db.Text)   # JSON list of choices
    correct_index = db.Column(db.Integer) # index into choices_json
    marks = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_choices(self):
        try:
            return json.loads(self.choices_json or "[]")
        except Exception:
            return []

