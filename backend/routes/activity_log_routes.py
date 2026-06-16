from flask import Blueprint, jsonify
from models.activity_log import ActivityLog
from extensions import db

activity_log_bp = Blueprint(
    "activity_log_bp",
    __name__
)


@activity_log_bp.route("/activity-logs", methods=["GET"])
def get_logs():

    logs = ActivityLog.query.order_by(
        ActivityLog.created_at.desc()
    ).all()

    return jsonify([
        {
            "id": log.id,
            "action": log.action,
            "description": log.description,
            "created_at": log.created_at
        }
        for log in logs
    ])


@activity_log_bp.route("/test-log", methods=["GET"])
def test_log():

    log = ActivityLog(
        action="Test Log",
        description="Testing activity log system"
    )

    db.session.add(log)
    db.session.commit()

    return jsonify({
        "message": "Log inserted successfully"
    })