from flask import Blueprint, request, jsonify
from models.purchase_order import PurchaseOrder
from models.approval import Approval
from models.quotation import Quotation
from extensions import db

purchase_order_bp = Blueprint(
    "purchase_order_bp",
    __name__
)


@purchase_order_bp.route("/purchase-orders", methods=["POST"])
def create_purchase_order():

    data = request.get_json()

    approval_id = data.get("approval_id")

    approval = Approval.query.get(approval_id)

    if not approval:
        return jsonify({"message": "Approval not found"}), 404

    if approval.status != "APPROVED":
        return jsonify({"message": "Approval is not approved"}), 400

    quotation = Quotation.query.filter_by(
        rfq_id=approval.rfq_id,
        vendor_id=approval.vendor_id
    ).first()

    if not quotation:
        return jsonify({"message": "Quotation not found"}), 404

    po = PurchaseOrder(
        po_number=f"PO-{approval.id}",
        rfq_id=approval.rfq_id,
        vendor_id=approval.vendor_id,
        total_amount=quotation.price,
        status="CREATED"
    )

    db.session.add(po)
    db.session.commit()

    return jsonify({
        "message": "Purchase Order created",
        "po_number": po.po_number
    }), 201


@purchase_order_bp.route("/purchase-orders", methods=["GET"])
def get_purchase_orders():

    orders = PurchaseOrder.query.all()

    return jsonify([
        {
            "id": po.id,
            "po_number": po.po_number,
            "rfq_id": po.rfq_id,
            "vendor_id": po.vendor_id,
            "total_amount": po.total_amount,
            "status": po.status
        }
        for po in orders
    ])