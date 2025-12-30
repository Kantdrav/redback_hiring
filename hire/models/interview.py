from datetime import datetime
from .db import db

class Interview(db.Model):
    __tablename__ = "interviews"
    id = db.Column(db.Integer, primary_key=True)
    round_id = db.Column(db.Integer, db.ForeignKey("rounds.id"))
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"))
    interviewer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    scheduled_at_utc = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, default=30)  # minutes
    status = db.Column(db.String(50), default="scheduled")  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # convenience relationships
    round = db.relationship("Round", backref="interviews", lazy=True)
    candidate = db.relationship("Candidate", backref="interviews", lazy=True)
    interviewer = db.relationship("User", backref="interviews_conducted", lazy=True)
