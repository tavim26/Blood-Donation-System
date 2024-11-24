from database import db


class User(db.Model):
    __tablename__ = 'User'
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Role = db.Column(db.String, nullable=False)
    FirstName = db.Column(db.String, nullable=False)
    LastName = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, unique=True, nullable=False)
    Password = db.Column(db.String, nullable=False)
    CNP = db.Column(db.String(13), unique=True, nullable=False)

    def __init__(self, first_name, last_name, email, password, cnp, role):
        self.FirstName = first_name
        self.LastName = last_name
        self.Email = email
        self.Password = password
        self.CNP = cnp
        self.Role = role
