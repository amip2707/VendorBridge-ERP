from flask import Blueprint, jsonify
from models.notification import Notification

notification_bp = Blueprint("notification_bp", __name__)


@notification_bp.route("/notifications", methods=["GET"])
def get_notifications():

    notifications = Notification.query.order_by(
        Notification.created_at.desc()
    ).all()

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        }
        for n in notifications
    ])
