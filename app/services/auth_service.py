from ..models.user_model import get_user_by_email, create_user
from ..utils.password_utils import hash_password, verify_password
from ..extensions.mongo import get_db

def register_user(name, email, password):
    if not email:
        return False, "Email is required"

    email = email.lower()

    if get_user_by_email(email):
        return False, "User already exists"

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password)
    }

    create_user(user)
    return True, "User registered successfully"


def login_user(email, password):
    db = get_db()
    user = db.users.find_one({"email": email})

    if not user:
        return False, "Invalid credentials"

    if not verify_password(user["password"], password):
        return False, "Invalid credentials"

    # ✅ IMPORTANT: convert ObjectId to string
    safe_user = {
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

    return True, safe_user
