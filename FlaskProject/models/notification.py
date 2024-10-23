from database import db

class Notification(db.Model):
    __tablename__ = 'Notification'
    NotificationID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DonorID = db.Column(db.Integer, db.ForeignKey('Donor.DonorID', ondelete='CASCADE'))
    NotificationType = db.Column(db.String(50), nullable=False)
    Message = db.Column(db.Text, nullable=False)

