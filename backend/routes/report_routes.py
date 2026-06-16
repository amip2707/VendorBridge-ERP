from flask import Blueprint, jsonify
from models.invoice import Invoice
from models.purchase_order import PurchaseOrder

report_bp = Blueprint(
    "report_bp",
    __name__
)


@report_bp.route("/reports/summary", methods=["GET"])
def procurement_summary():

    total_pos = PurchaseOrder.query.count()

    total_invoices = Invoice.query.count()

    total_spend = sum(
        invoice.total_amount
        for invoice in Invoice.query.all()
    )

    return jsonify({
        "total_purchase_orders": total_pos,
        "total_invoices": total_invoices,
        "total_spending": total_spend
    })