from database import db


class Report(db.Model):
    __tablename__ = 'Report'
    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AssistantID = db.Column(db.Integer, db.ForeignKey('Assistant.AssistantID', ondelete='SET NULL'), nullable=True)
    DonationID = db.Column(db.Integer, db.ForeignKey('Donation.DonationID', ondelete='SET NULL'), nullable=True)
    ReportType = db.Column(db.String(50), nullable=False)
    ReportData = db.Column(db.Text, nullable=False)

    donation = db.relationship('Donation', backref='reports')
    assistant = db.relationship('Assistant', backref='reports')
