from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/test")
def test():
    return {
        "message": "Auth route working"
    }

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({
            "status": "error",
            "message": "Email already exists"
        }), 400

    hashed_password = generate_password_hash(password)

    user = User(
        full_name=full_name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": "User registered successfully"
    }), 201