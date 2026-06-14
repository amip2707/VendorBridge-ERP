from extensions import db
from datetime import datetime

class RFQ(db.Model):
    __tablename__ = "rfqs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)