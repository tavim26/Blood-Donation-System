from database import db

class Schedule(db.Model):
    __tablename__ = 'Schedule'
    ScheduleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    AppointmentDate = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(10), default='pending', nullable=False)

    __table_args__ = (
        db.CheckConstraint("Status IN ('pending', 'canceled')"),
    )
