from extensions import db


class Authentication(db.Model):
    __tablename__ = 'Authentication'
    AuthID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('Authentications', lazy=True))

    def __init__(self, user_id, token=False):
        self.UserID = user_id
        self.token = token
