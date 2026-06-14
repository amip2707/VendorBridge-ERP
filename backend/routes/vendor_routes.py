from flask import Blueprint, request, jsonify
from models.vendor import Vendor
from extensions import db

vendor_bp = Blueprint("vendor_bp", __name__)


@vendor_bp.route("/vendors", methods=["POST"])
def add_vendor():
    data = request.get_json()

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
    db.session.commit()

    return jsonify({"message": "Vendor added successfully"}), 201


@vendor_bp.route("/vendors", methods=["GET"])
def get_vendors():
    vendors = Vendor.query.all()

    result = []

    for v in vendors:
        result.append({
            "id": v.id,
            "company_name": v.company_name,
            "contact_person": v.contact_person,
            "email": v.email,
            "phone": v.phone,
            "address": v.address,
            "gst_number": v.gst_number,
            "status": v.status,
            "created_at": v.created_at
        })

    return jsonify(result)