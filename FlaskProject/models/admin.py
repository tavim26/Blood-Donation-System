from database import db


class Admin(db.Model):
    __tablename__ = 'Admin'
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', backref='admin', uselist=False)

    def __init__(self, admin_id):
        self.UserID = admin_id
