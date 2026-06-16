from flask import Blueprint, request, jsonify
from models.rfq import RFQ
from models.activity_log import ActivityLog
from extensions import db

rfq_bp = Blueprint("rfq_bp", __name__)


@rfq_bp.route("/rfqs", methods=["POST"])
def create_rfq():
    data = request.get_json()

    new_rfq = RFQ(
        title=data.get("title"),
        description=data.get("description"),
        quantity=data.get("quantity"),
        deadline=data.get("deadline")
    )

    db.session.add(new_rfq)
    db.session.commit()

    log = ActivityLog(
        action="RFQ Created",
        description=f"RFQ '{new_rfq.title}' created successfully"
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "RFQ created successfully"
    }), 201


@rfq_bp.route("/rfqs", methods=["GET"])
def get_rfqs():
    rfqs = RFQ.query.all()

    return jsonify([
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "quantity": r.quantity,
            "deadline": str(r.deadline),
            "status": r.status
        }
        for r in rfqs
    ])


@rfq_bp.route("/rfqs/<int:rfq_id>", methods=["GET"])
def get_rfq(rfq_id):
    rfq = RFQ.query.get(rfq_id)

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    return jsonify({
        "id": rfq.id,
        "title": rfq.title,
        "description": rfq.description,
        "quantity": rfq.quantity,
        "deadline": str(rfq.deadline),
        "status": rfq.status
    })


@rfq_bp.route("/rfqs/<int:rfq_id>", methods=["DELETE"])
def delete_rfq(rfq_id):
    rfq = RFQ.query.get(rfq_id)

    if not rfq:
        return jsonify({
            "message": "RFQ not found"
        }), 404

    db.session.delete(rfq)
    db.session.commit()

    log = ActivityLog(
        action="RFQ Deleted",
        description=f"RFQ '{rfq.title}' deleted"
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "RFQ deleted successfully"
    })