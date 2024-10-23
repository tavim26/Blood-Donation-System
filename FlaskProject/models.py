from sqlalchemy import func

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

from sqlalchemy import func  # Asigură-te că ai importat func din SQLAlchemy

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


class BloodStock(db.Model):
    __tablename__ = 'BloodStock'
    BloodGroup = db.Column(db.String(5), primary_key=True, nullable=False)
    QuantityInStock = db.Column(db.Integer, default=0)


class Schedule(db.Model):
    __tablename__ = 'Schedule'
    ScheduleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    AppointmentDate = db.Column(db.DateTime, nullable=False)
    Status = db.Column(db.String(10), default='pending', nullable=False)

    __table_args__ = (
        db.CheckConstraint("Status IN ('pending', 'canceled')"),
    )


class Reward(db.Model):
    __tablename__ = 'Reward'
    RewardID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    RewardDescription = db.Column(db.Text, nullable=False)
    RewardDate = db.Column(db.Date, nullable=False)


class EligibilityForm(db.Model):
    __tablename__ = 'EligibilityForm'
    FormID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'), nullable=False)
    BloodGroup = db.Column(db.String(5), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    Weight = db.Column(db.Integer, nullable=False)
    Notes = db.Column(db.Text, nullable=False)
    IsEligible = db.Column(db.Boolean, default=True)


class Report(db.Model):
    __tablename__ = 'Report'
    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssistantID = db.Column(db.Integer, db.ForeignKey('Assistant.AssistantID', ondelete='SET NULL'), nullable=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='SET NULL'), nullable=True)
    ReportType = db.Column(db.String(50), nullable=False)
    ReportData = db.Column(db.Text, nullable=False)


class Notification(db.Model):
    __tablename__ = 'Notification'
    NotificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'))
    NotificationType = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.Text, nullable=False)


class ActivityLog(db.Model):
    __tablename__ = 'ActivityLog'
    ActivityLogID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('User.UserID', ondelete='CASCADE'), nullable=False)
    Action = db.Column(db.Text, nullable=False)
    Timestamp = db.Column(db.DateTime, default=func.now(), nullable=False)  # Adăugat timestamp
