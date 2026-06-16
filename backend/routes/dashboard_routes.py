from flask import Blueprint, jsonify

from models.vendor import Vendor
from models.rfq import RFQ
from models.quotation import Quotation
from models.approval import Approval
from models.purchase_order import PurchaseOrder
from models.invoice import Invoice

dashboard_bp = Blueprint(
    "dashboard_bp",
    __name__
)


@dashboard_bp.route("/dashboard", methods=["GET"])
def dashboard():

    total_vendors = Vendor.query.count()

    total_rfqs = RFQ.query.count()

    total_quotations = Quotation.query.count()

    pending_approvals = Approval.query.filter_by(
        status="PENDING"
    ).count()

    approved_approvals = Approval.query.filter_by(
        status="APPROVED"
    ).count()

    total_purchase_orders = PurchaseOrder.query.count()

    total_invoices = Invoice.query.count()

    return jsonify({
        "total_vendors": total_vendors,
        "total_rfqs": total_rfqs,
        "total_quotations": total_quotations,
        "pending_approvals": pending_approvals,
        "approved_approvals": approved_approvals,
        "total_purchase_orders": total_purchase_orders,
        "total_invoices": total_invoices
    })