"""HR Models - Interview Plans, Schedules, Test Results"""
from .db import db
from datetime import datetime
import json


class InterviewPlan(db.Model):
    __tablename__ = "interview_plans"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    round_order_json = db.Column(db.Text, default='[]')
    status = db.Column(db.String(50), default="draft")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = db.relationship("Job", backref="interview_plans")

    def get_rounds(self):
        try:
            return json.loads(self.round_order_json or "[]")
        except Exception:
            return []


class InterviewSchedule(db.Model):
    __tablename__ = "interview_schedules"
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    interview_plan_id = db.Column(db.Integer, db.ForeignKey("interview_plans.id"), nullable=False)
    current_round_index = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default="invited")
    invited_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    feedback_json = db.Column(db.Text)

    candidate = db.relationship("Candidate", backref="interview_schedules")
    interview_plan = db.relationship("InterviewPlan", backref="schedules")


class CandidateTestResult(db.Model):
    __tablename__ = "candidate_test_results"
    id = db.Column(db.Integer, primary_key=True)
    interview_schedule_id = db.Column(db.Integer, db.ForeignKey("interview_schedules.id"), nullable=False)
    round_index = db.Column(db.Integer)
    round_type = db.Column(db.String(50))
    language_tested = db.Column(db.String(100))
    score = db.Column(db.Float, nullable=True)
    max_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50))
    test_data_json = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    schedule = db.relationship("InterviewSchedule", backref="test_results")
