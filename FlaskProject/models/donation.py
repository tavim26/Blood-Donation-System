from extensions import db


class Donation(db.Model):
    __tablename__ = 'Donation'
    DonationName = db.Column(db.String)
    DonationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ScheduleID = db.Column(db.Integer, db.ForeignKey('Schedule.ScheduleID', ondelete='CASCADE'))
    BloodGroup = db.Column(db.String(5), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    DonationDate = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(10), nullable=False)
    Notes = db.Column(db.Text)

    schedule = db.relationship('Schedule', backref='donations')

    __table_args__ = (
        db.CheckConstraint("Status IN ('completed', 'returned', 'pending')"),
    )
