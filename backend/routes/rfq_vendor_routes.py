from flask import Blueprint, request, jsonify
from models.rfq_vendor import RFQVendor
from models.rfq import RFQ
from models.vendor import Vendor
from models.activity_log import ActivityLog
from models.notification import Notification
from extensions import db

rfq_vendor_bp = Blueprint("rfq_vendor_bp", __name__)


@rfq_vendor_bp.route("/rfq/assign", methods=["POST"])
def assign_vendor():
    data = request.get_json()

    rfq_id = data.get("rfq_id")
    vendor_id = data.get("vendor_id")

    if not rfq_id or not vendor_id:
        return jsonify({"message": "rfq_id and vendor_id are required"}), 400

    rfq = RFQ.query.get(rfq_id)
    if not rfq:
        return jsonify({"message": "RFQ not found"}), 404

    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({"message": "Vendor not found"}), 404

    existing = RFQVendor.query.filter_by(
        rfq_id=rfq_id,
        vendor_id=vendor_id
    ).first()

    if existing:
        return jsonify({"message": "Vendor already assigned to this RFQ"}), 409

    mapping = RFQVendor(
        rfq_id=rfq_id,
        vendor_id=vendor_id
    )

    db.session.add(mapping)

    log = ActivityLog(
        action="Vendor Assigned",
        description=f"Vendor {vendor.company_name} assigned to RFQ {rfq.title}"
    )

    notification = Notification(
        title="Vendor Assigned",
        message=f"{vendor.company_name} assigned to RFQ '{rfq.title}'"
    )

    db.session.add(log)
    db.session.add(notification)

    db.session.commit()

    return jsonify({
        "message": "Vendor assigned to RFQ successfully",
        "rfq_id": rfq_id,
        "vendor_id": vendor_id
    }), 201


@rfq_vendor_bp.route("/rfq/<int:rfq_id>/vendors", methods=["GET"])
def get_assigned_vendors(rfq_id):
    mappings = RFQVendor.query.filter_by(rfq_id=rfq_id).all()

    return jsonify([
        {
            "id": m.id,
            "rfq_id": m.rfq_id,
            "vendor_id": m.vendor_id
        }
        for m in mappings
    ])