from datetime import datetime
from .db import db

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    dept = db.Column(db.String(100))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    status = db.Column(db.String(30), default="open")  # open/closed
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
