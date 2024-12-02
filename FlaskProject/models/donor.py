from extensions import db


class Donor(db.Model):
    __tablename__ = 'Donor'
    DonorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)
    BloodGroup = db.Column(db.String, nullable=False)
    Age = db.Column(db.String, nullable=False)
    Gender = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='donor', uselist=False)

    def __init__(self, donor_id, blood_group, age, gender):
        self.UserID = donor_id
        self.BloodGroup = blood_group
        self.Age = age
        self.Gender = gender
