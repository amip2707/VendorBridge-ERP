from extensions import db
from datetime import datetime

class Approval(db.Model):
    __tablename__ = "approvals"

    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(db.Integer, db.ForeignKey("rfqs.id"), nullable=False)

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)

    status = db.Column(db.String(20), default="PENDING")

    remarks = db.Column(db.Text)

    approved_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)