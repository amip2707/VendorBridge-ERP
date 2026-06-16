from extensions import db
from datetime import datetime

class PurchaseOrder(db.Model):
    __tablename__ = "purchase_orders"

    id = db.Column(db.Integer, primary_key=True)

    po_number = db.Column(db.String(50), unique=True)

    rfq_id = db.Column(db.Integer, db.ForeignKey("rfqs.id"), nullable=False)

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)

    total_amount = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(20), default="CREATED")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)