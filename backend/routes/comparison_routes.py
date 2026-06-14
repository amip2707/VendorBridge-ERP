from flask import Blueprint, jsonify
from models.quotation import Quotation

comparison_bp = Blueprint("comparison_bp", __name__)


@comparison_bp.route("/rfq/<int:rfq_id>/compare", methods=["GET"])
def compare_rfq(rfq_id):
    quotes = Quotation.query.filter_by(rfq_id=rfq_id).all()

    if not quotes:
        return jsonify({"message": "No quotations found"}), 404

    lowest_price = min(quotes, key=lambda x: x.price)
    fastest_delivery = min(quotes, key=lambda x: x.delivery_days)

    return jsonify({
        "rfq_id": rfq_id,
        "lowest_price": {
            "vendor_id": lowest_price.vendor_id,
            "price": lowest_price.price
        },
        "fastest_delivery": {
            "vendor_id": fastest_delivery.vendor_id,
            "delivery_days": fastest_delivery.delivery_days
        },
        "all_quotes": [
            {
                "vendor_id": q.vendor_id,
                "price": q.price,
                "delivery_days": q.delivery_days
            }
            for q in quotes
        ]
    })