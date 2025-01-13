from sqlalchemy import func
from extensions import db


class ActivityLog(db.Model):
    __tablename__ = 'ActivityLog'
    ActivityLogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Action = db.Column(db.Text, nullable=False)
    Timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)

