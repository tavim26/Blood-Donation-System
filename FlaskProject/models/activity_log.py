from sqlalchemy import func
from database import db

class ActivityLog(db.Model):
    __tablename__ = 'ActivityLog'
    ActivityLogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)
    Action = db.Column(db.Text, nullable=False)
    Timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)

    user = db.relationship('User', backref='activity_logs')