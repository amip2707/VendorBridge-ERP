from flask import Blueprint, request, jsonify
from models.quotation import Quotation
from extensions import db

quotation_bp = Blueprint("quotation_bp", __name__)


@quotation_bp.route("/quotations", methods=["POST"])
def add_quotation():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    required_fields = ["rfq_id", "vendor_id", "price", "delivery_days"]

    for field in required_fields:
        if data.get(field) is None:
            return jsonify({"error": f"{field} is required"}), 400

    quotation = Quotation(
        rfq_id=data.get("rfq_id"),
        vendor_id=data.get("vendor_id"),
        price=data.get("price"),
        delivery_days=data.get("delivery_days"),
        notes=data.get("notes")
    )

    db.session.add(quotation)
    db.session.commit()

    return jsonify({"message": "Quotation submitted"}), 201


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
        }
    })