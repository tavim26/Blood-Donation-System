from database import db


class BloodStock(db.Model):
    __tablename__ = 'BloodStock'
    BloodGroup = db.Column(db.String(5), primary_key=True, nullable=False)
    QuantityInStock = db.Column(db.Integer, default=0)
