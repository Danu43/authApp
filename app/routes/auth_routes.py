from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"message": "name, email and password are required"}), 400

    success, msg = register_user(name, email, password)
    return jsonify({"message": msg}), 201 if success else 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not all([email, password]):
        return jsonify({"message": "email and password are required"}), 400

    success, result = login_user(email, password)

    if not success:
        return jsonify({"message": result}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "name": result["name"],
            "email": result["email"]
        }
    }), 200
