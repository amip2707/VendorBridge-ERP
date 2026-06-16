from extensions import db
from datetime import datetime

class Invoice(db.Model):
    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True)

    invoice_number = db.Column(db.String(50), unique=True)

    po_id = db.Column(
        db.Integer,
        db.ForeignKey("purchase_orders.id"),
        nullable=False
    )

    amount = db.Column(db.Float, nullable=False)

    tax = db.Column(db.Float, default=18)

    total_amount = db.Column(db.Float)

    status = db.Column(db.String(20), default="GENERATED")

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )