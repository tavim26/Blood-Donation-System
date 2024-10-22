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


class Admin(db.Model):
    __tablename__ = 'Admin'
    AdminID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)

    user = db.relationship('User', backref='admin', uselist=False)

    def __init__(self, admin_id):
        self.UserID = admin_id


class Assistant(db.Model):
    __tablename__ = 'Assistant'
    AssistantID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)

    user = db.relationship('User', backref='assistant', uselist=False)

    def __init__(self, assistant_id):
        self.UserID = assistant_id


class Donor(db.Model):
    __tablename__ = 'Donor'
    DonorID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID'), nullable=False)
    BloodGroup = db.Column(db.String, nullable=False)
    Age = db.Column(db.String, nullable=False)
    Gender = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='donor', uselist=False)

    def __init__(self, donor_id, blood_group, age, gender):
        self.UserID = donor_id
        self.BloodGroup = blood_group
        self.Age = age
        self.Gender = gender
