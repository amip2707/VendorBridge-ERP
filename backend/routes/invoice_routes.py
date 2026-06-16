from flask import Blueprint, request, jsonify
from models.invoice import Invoice
from models.purchase_order import PurchaseOrder
from extensions import db

invoice_bp = Blueprint(
    "invoice_bp",
    __name__
)


@invoice_bp.route("/invoices", methods=["POST"])
def create_invoice():

    data = request.get_json()

    po_id = data.get("po_id")

    po = PurchaseOrder.query.get(po_id)

    if not po:
        return jsonify({
            "message": "Purchase Order not found"
        }), 404

    amount = po.total_amount
    tax = 18
    total_amount = amount + (amount * tax / 100)

    invoice = Invoice(
        invoice_number=f"INV-{po.id}",
        po_id=po.id,
        amount=amount,
        tax=tax,
        total_amount=total_amount
    )

    db.session.add(invoice)
    db.session.commit()

    return jsonify({
        "message": "Invoice generated",
        "invoice_number": invoice.invoice_number,
        "total_amount": total_amount
    }), 201


@invoice_bp.route("/invoices", methods=["GET"])
def get_invoices():

    invoices = Invoice.query.all()

    return jsonify([
        {
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "po_id": inv.po_id,
            "amount": inv.amount,
            "tax": inv.tax,
            "total_amount": inv.total_amount,
            "status": inv.status
        }
        for inv in invoices
    ])