from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(180), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(120))
    role = db.Column(db.String(30), default="candidate")  # admin, hr, interviewer, candidate
    phone = db.Column(db.String(30))
    is_active = db.Column(db.Boolean, default=True)
    permissions_json = db.Column(db.Text, default='{}')  # JSON for granular permissions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    def get_permissions(self):
        try:
            return json.loads(self.permissions_json or "{}")
        except Exception:
            return {}

    def set_permissions(self, perms_dict):
        self.permissions_json = json.dumps(perms_dict)

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    action = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    payload_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Phase 2 Models
class Round(db.Model):
    __tablename__ = "rounds"
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, nullable=True)  # in future: FK to interview_plans
    order_index = db.Column(db.Integer, default=0)
    name = db.Column(db.String(200))
    type = db.Column(db.String(50))  # hr, technical, mcq, coding, live
    duration_minutes = db.Column(db.Integer, default=30)
    config_json = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_config(self):
        try:
            return json.loads(self.config_json or "{}")
        except Exception:
            return {}

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


# Admin Models for Question Banks and Scoring Policies
class ProgrammingLanguage(db.Model):
    __tablename__ = "programming_languages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # Python, Java, JavaScript, etc.
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class QuestionBank(db.Model):
    __tablename__ = "question_banks"
    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("programming_languages.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    question_count = db.Column(db.Integer, default=0)
    enabled = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    language = db.relationship("ProgrammingLanguage", backref="question_banks")


class QuestionBankItem(db.Model):
    __tablename__ = "question_bank_items"
    id = db.Column(db.Integer, primary_key=True)
    bank_id = db.Column(db.Integer, db.ForeignKey("question_banks.id"), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), default="mcq")  # mcq, coding, essay
    difficulty = db.Column(db.String(20), default="medium")  # easy, medium, hard
    choices_json = db.Column(db.Text)  # For MCQ
    correct_answer = db.Column(db.Text)  # For coding/essay
    time_limit_seconds = db.Column(db.Integer, default=300)
    enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_choices(self):
        try:
            return json.loads(self.choices_json or "[]")
        except Exception:
            return []


class ScoringPolicy(db.Model):
    __tablename__ = "scoring_policies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    policy_json = db.Column(db.Text)  # JSON config: weights, passing_score, rubric, etc.
    enabled = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_policy(self):
        try:
            return json.loads(self.policy_json or "{}")
        except Exception:
            return {}


class RoundTemplate(db.Model):
    __tablename__ = "round_templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # hr, technical, mcq, coding, live
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=30)
    config_json = db.Column(db.Text, default='{}')  # Template-specific config
    enabled = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_config(self):
        try:
            return json.loads(self.config_json or "{}")
        except Exception:
            return {}


class InterviewPlan(db.Model):
    __tablename__ = "interview_plans"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    round_order_json = db.Column(db.Text, default='[]')  # JSON list of round configs
    status = db.Column(db.String(50), default="draft")  # draft, active, archived
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
    status = db.Column(db.String(50), default="invited")  # invited, in_progress, completed, rejected
    invited_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    feedback_json = db.Column(db.Text)  # Per-round feedback

    candidate = db.relationship("Candidate", backref="interview_schedules")
    interview_plan = db.relationship("InterviewPlan", backref="schedules")


class CandidateTestResult(db.Model):
    __tablename__ = "candidate_test_results"
    id = db.Column(db.Integer, primary_key=True)
    interview_schedule_id = db.Column(db.Integer, db.ForeignKey("interview_schedules.id"), nullable=False)
    round_index = db.Column(db.Integer)
    round_type = db.Column(db.String(50))
    language_tested = db.Column(db.String(100))  # For technical rounds
    score = db.Column(db.Float, nullable=True)
    max_score = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50))  # passed, failed, pending_review
    test_data_json = db.Column(db.Text)  # Responses, timing, etc.
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    schedule = db.relationship("InterviewSchedule", backref="test_results")