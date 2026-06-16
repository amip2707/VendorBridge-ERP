from flask import Blueprint, request, jsonify
from models.vendor import Vendor
from models.activity_log import ActivityLog
from models.notification import Notification
from extensions import db

vendor_bp = Blueprint("vendor_bp", __name__)


@vendor_bp.route("/vendors", methods=["POST"])
def add_vendor():
    data = request.get_json()

    if not data.get("company_name") or not data.get("email"):
        return jsonify({"error": "company_name and email required"}), 400

    existing = Vendor.query.filter_by(email=data.get("email")).first()
    if existing:
        return jsonify({"error": "Vendor already exists"}), 409

    new_vendor = Vendor(
        company_name=data.get("company_name"),
        contact_person=data.get("contact_person"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address"),
        gst_number=data.get("gst_number"),
        status=data.get("status", "Pending")
    )

    db.session.add(new_vendor)

    log = ActivityLog(
        action="Vendor Created",
        description=f"Vendor '{new_vendor.company_name}' registered successfully"
    )

    notification = Notification(
        title="Vendor Added",
        message=f"Vendor '{new_vendor.company_name}' has been added"
    )

    db.session.add(log)
    db.session.add(notification)

    db.session.commit()

    return jsonify({
        "message": "Vendor added successfully",
        "vendor_id": new_vendor.id
    }), 201


@vendor_bp.route("/vendors", methods=["GET"])
def get_vendors():
    vendors = Vendor.query.all()

    return jsonify([
        {
            "id": v.id,
            "company_name": v.company_name,
            "contact_person": v.contact_person,
            "email": v.email,
            "phone": v.phone,
            "address": v.address,
            "gst_number": v.gst_number,
            "status": v.status,
            "created_at": v.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for v in vendors
    ])