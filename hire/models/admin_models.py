"""Admin Models - Question Banks, Languages, Scoring Policies, Round Templates"""
from .db import db
from datetime import datetime
import json


class ProgrammingLanguage(db.Model):
    __tablename__ = "programming_languages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
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
    question_type = db.Column(db.String(50), default="mcq")
    difficulty = db.Column(db.String(20), default="medium")
    choices_json = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
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
    policy_json = db.Column(db.Text)
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
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, default=30)
    config_json = db.Column(db.Text, default='{}')
    enabled = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_config(self):
        try:
            return json.loads(self.config_json or "{}")
        except Exception:
            return {}


class WebsiteVisit(db.Model):
    """Track website visits and page views"""
    __tablename__ = "website_visits"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(500))
    endpoint = db.Column(db.String(255))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)
    response_time_ms = db.Column(db.Float)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="visits")


class UserImpersonation(db.Model):
    """Audit log for admin impersonation actions"""
    __tablename__ = "user_impersonations"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details_json = db.Column(db.Text, default='{}')
    status = db.Column(db.String(50), default="success")
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    admin = db.relationship("User", foreign_keys=[admin_id], backref="admin_impersonations")
    target_user = db.relationship("User", foreign_keys=[target_user_id], backref="impersonated_by")
