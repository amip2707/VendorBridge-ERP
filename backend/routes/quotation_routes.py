from flask import Blueprint, request, jsonify
from models.quotation import Quotation
from models.rfq_vendor import RFQVendor
from models.rfq import RFQ
from models.vendor import Vendor
from models.activity_log import ActivityLog
from models.notification import Notification
from extensions import db

quotation_bp = Blueprint("quotation_bp", __name__)


@quotation_bp.route("/quotations", methods=["POST"])
def add_quotation():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    rfq_id = data.get("rfq_id")
    vendor_id = data.get("vendor_id")

    if not rfq_id or not vendor_id:
        return jsonify({"error": "rfq_id and vendor_id are required"}), 400

    rfq = RFQ.query.get(rfq_id)
    if not rfq:
        return jsonify({"error": "RFQ not found"}), 404

    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404

    assigned = RFQVendor.query.filter_by(
        rfq_id=rfq_id,
        vendor_id=vendor_id
    ).first()

    if not assigned:
        return jsonify({"error": "Vendor not assigned to this RFQ"}), 403

    existing_quote = Quotation.query.filter_by(
        rfq_id=rfq_id,
        vendor_id=vendor_id
    ).first()

    if existing_quote:
        return jsonify({"error": "Quotation already submitted"}), 409

    quotation = Quotation(
        rfq_id=rfq_id,
        vendor_id=vendor_id,
        price=data.get("price"),
        delivery_days=data.get("delivery_days"),
        notes=data.get("notes")
    )

    db.session.add(quotation)

    log = ActivityLog(
        action="Quotation Submitted",
        description=f"Vendor {vendor.company_name} submitted quotation for RFQ {rfq.title}"
    )

    notification = Notification(
        title="New Quotation",
        message=f"{vendor.company_name} submitted quotation for RFQ '{rfq.title}'"
    )

    db.session.add(log)
    db.session.add(notification)

    db.session.commit()

    return jsonify({
        "message": "Quotation submitted successfully",
        "rfq_id": rfq_id,
        "vendor_id": vendor_id
    }), 201


@quotation_bp.route("/quotations/<int:rfq_id>", methods=["GET"])
def get_quotations(rfq_id):
    quotes = Quotation.query.filter_by(rfq_id=rfq_id).all()

    return jsonify([
        {
            "vendor_id": q.vendor_id,
            "price": q.price,
            "delivery_days": q.delivery_days,
            "notes": q.notes
        }
        for q in quotes
    ])


@quotation_bp.route("/quotations/summary/<int:rfq_id>", methods=["GET"])
def quotation_summary(rfq_id):
    quotes = Quotation.query.filter_by(rfq_id=rfq_id).all()

    if not quotes:
        return jsonify({"message": "No quotations found"}), 404

    lowest = min(quotes, key=lambda q: q.price)
    fastest = min(quotes, key=lambda q: q.delivery_days)

    return jsonify({
        "rfq_id": rfq_id,
        "lowest_price": {
            "vendor_id": lowest.vendor_id,
            "price": lowest.price
        },
        "fastest_delivery": {
            "vendor_id": fastest.vendor_id,
            "delivery_days": fastest.delivery_days
        },
        "all_quotes": [
            {
                "vendor_id": q.vendor_id,
                "price": q.price,
                "delivery_days": q.delivery_days,
                "notes": q.notes
            }
            for q in quotes
        ]
    })