from database import db


class Assistant(db.Model):
    __tablename__ = 'Assistant'
    AssistantID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)

    user = db.relationship('User', backref='assistant', uselist=False)

    def __init__(self, assistant_id):
        self.UserID = assistant_id
