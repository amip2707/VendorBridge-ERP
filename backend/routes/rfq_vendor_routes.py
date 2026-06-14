from flask import Blueprint, request, jsonify
from models.rfq_vendor import RFQVendor
from extensions import db

rfq_vendor_bp = Blueprint("rfq_vendor_bp", __name__)


@rfq_vendor_bp.route("/rfq/assign", methods=["POST"])
def assign_vendor():
    data = request.get_json()

    mapping = RFQVendor(
        rfq_id=data.get("rfq_id"),
        vendor_id=data.get("vendor_id")
    )

    db.session.add(mapping)
    db.session.commit()

    return jsonify({"message": "Vendor assigned to RFQ"}), 201


@rfq_vendor_bp.route("/rfq/<int:rfq_id>/vendors", methods=["GET"])
def get_assigned_vendors(rfq_id):
    mappings = RFQVendor.query.filter_by(rfq_id=rfq_id).all()

    result = []
    for m in mappings:
        result.append({
            "id": m.id,
            "rfq_id": m.rfq_id,
            "vendor_id": m.vendor_id
        })

    return jsonify(result)