from database import db

class Donation(db.Model):
    __tablename__ = 'Donation'
    DonationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    AssistantID = db.Column(db.Integer, db.ForeignKey('Assistant.AssistantID', ondelete='SET NULL'))
    BloodGroup = db.Column(db.String(5), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    DonationDate = db.Column(db.Date, nullable=False)
    Status = db.Column(db.String(10), nullable=False)
    Notes = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("Status IN ('completed', 'returned')"),
    )
