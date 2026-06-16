from flask import Blueprint, request, jsonify
from models.approval import Approval
from extensions import db
from datetime import datetime

approval_bp = Blueprint("approval_bp", __name__)


@approval_bp.route("/approvals", methods=["POST"])
def create_approval():
    data = request.get_json()

    approval = Approval(
        rfq_id=data.get("rfq_id"),
        vendor_id=data.get("vendor_id"),
        remarks=data.get("remarks"),
        status="PENDING"
    )

    db.session.add(approval)
    db.session.commit()

    return jsonify({
        "message": "Approval request created"
    }), 201


@approval_bp.route("/approvals/<int:approval_id>/approve", methods=["PUT"])
def approve_request(approval_id):
    approval = Approval.query.get(approval_id)

    if not approval:
        return jsonify({"message": "Approval not found"}), 404

    approval.status = "APPROVED"
    approval.approved_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        "message": "Quotation approved"
    })


@approval_bp.route("/approvals/<int:approval_id>/reject", methods=["PUT"])
def reject_request(approval_id):
    approval = Approval.query.get(approval_id)

    if not approval:
        return jsonify({"message": "Approval not found"}), 404

    approval.status = "REJECTED"

    db.session.commit()

    return jsonify({
        "message": "Quotation rejected"
    })


@approval_bp.route("/approvals", methods=["GET"])
def get_approvals():
    approvals = Approval.query.all()

    return jsonify([
        {
            "id": a.id,
            "rfq_id": a.rfq_id,
            "vendor_id": a.vendor_id,
            "status": a.status,
            "remarks": a.remarks
        }
        for a in approvals
    ])