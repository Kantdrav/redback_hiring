from datetime import datetime
from .db import db

class Candidate(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    name = db.Column(db.String(200))
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    resume_path = db.Column(db.String(500))
    applied_job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    status = db.Column(db.String(50), default="applied")
    match_score = db.Column(db.Integer, default=0)  # 0-100
    experience_years = db.Column(db.Float, default=0)  # Years of experience
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    job = db.relationship("Job", backref="candidates")
    user = db.relationship("User", backref="candidates")
    
    def get_experience_level(self):
        """Return experience level based on years: beginner (0-1), intermediate (1-3), advanced (3+)"""
        if self.experience_years is None:
            return "beginner"
        if self.experience_years < 1:
            return "beginner"
        elif self.experience_years < 3:
            return "intermediate"
        else:
            return "advanced"
