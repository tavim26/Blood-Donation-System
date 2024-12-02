from extensions import db


class Reward(db.Model):
    __tablename__ = 'Reward'
    RewardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    RewardDescription = db.Column(db.Text, nullable=False)
    RewardDate = db.Column(db.Date, nullable=False)
