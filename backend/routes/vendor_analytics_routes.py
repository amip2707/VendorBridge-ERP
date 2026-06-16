from flask import Blueprint, jsonify
from models.vendor import Vendor
from models.quotation import Quotation
from models.approval import Approval

vendor_analytics_bp = Blueprint(
    "vendor_analytics_bp",
    __name__
)


@vendor_analytics_bp.route(
    "/vendor-performance",
    methods=["GET"]
)
def vendor_performance():

    vendors = Vendor.query.all()

    result = []

    for vendor in vendors:

        total_quotes = Quotation.query.filter_by(
            vendor_id=vendor.id
        ).count()

        approved_quotes = Approval.query.filter_by(
            vendor_id=vendor.id,
            status="APPROVED"
        ).count()

        approval_rate = 0

        if total_quotes > 0:
            approval_rate = round(
                (approved_quotes / total_quotes) * 100,
                2
            )

        result.append({
            "vendor_id": vendor.id,
            "company_name": vendor.company_name,
            "quotations_submitted": total_quotes,
            "approvals_received": approved_quotes,
            "approval_rate": f"{approval_rate}%"
        })

    return jsonify(result)