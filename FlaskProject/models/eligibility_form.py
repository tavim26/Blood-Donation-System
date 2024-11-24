from database import db


class EligibilityForm(db.Model):
    __tablename__ = 'EligibilityForm'
    FormID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'))
    FormName = db.Column(db.String(50), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Weight = db.Column(db.Integer, nullable=False)
    Notes = db.Column(db.Text, nullable=False)
    IsEligible = db.Column(db.Boolean, default=True)

    donor = db.relationship('Donor', backref='eligibility_forms', lazy=True)
