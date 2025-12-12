from datetime import datetime
from .db import db

class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    action = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    payload_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
