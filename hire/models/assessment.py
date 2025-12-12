from datetime import datetime
import json
from .db import db

class Assessment(db.Model):
    __tablename__ = "assessments"
    id = db.Column(db.Integer, primary_key=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"))
    score_numeric = db.Column(db.Float, nullable=True)
    score_json = db.Column(db.Text)  # detailed rubric or MCQ result
    feedback_text = db.Column(db.Text)
    submitted_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_score_json(self):
        try:
            return json.loads(self.score_json or "{}")
        except Exception:
            return {}
