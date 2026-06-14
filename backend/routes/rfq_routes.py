from flask import Blueprint, request, jsonify
from models.rfq import RFQ
from extensions import db

rfq_bp = Blueprint("rfq_bp", __name__)

@rfq_bp.route("/rfqs", methods=["POST"])
def create_rfq():
    data = request.get_json()

    rfq = RFQ(
        title=data.get("title"),
        description=data.get("description"),
        quantity=data.get("quantity"),
        deadline=data.get("deadline")
    )

    db.session.add(rfq)
    db.session.commit()

    return jsonify({"message": "RFQ created successfully"}), 201


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