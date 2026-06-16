from extensions import db

class RFQVendor(db.Model):
    __tablename__ = "rfq_vendors"

    id = db.Column(db.Integer, primary_key=True)

    rfq_id = db.Column(db.Integer, db.ForeignKey("rfqs.id"), nullable=False)

    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)