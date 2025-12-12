from datetime import datetime
import json
from .db import db

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
