from flask import Blueprint, request, jsonify
from app.utils.validators import validate_email, validate_password, validate_name
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    # 1️⃣ Get JSON body
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    # 2️⃣ Validate name
    valid, name_or_error = validate_name(data.get("name"))
    if not valid:
        return jsonify({"message": name_or_error}), 400

    # 3️⃣ Validate email
    valid, email_or_error = validate_email(data.get("email"))
    if not valid:
        return jsonify({"message": email_or_error}), 400

    # 4️⃣ Validate password
    valid, password_error = validate_password(data.get("password"))
    if not valid:
        return jsonify({"message": password_error}), 400

    # 5️⃣ Register user
    success, msg = register_user(
        name_or_error,
        email_or_error,
        data.get("password")
    )

    return jsonify({"message": msg}), 201 if success else 400



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    success, result = login_user(email, password)

    if success:
        return jsonify({
            "message": "Login successful",
            "user": result
        }), 200

    return jsonify({"message": result}), 401
