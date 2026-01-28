from ..models.user_model import get_user_by_email, create_user
from ..utils.password_utils import hash_password, verify_password

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
    user = get_user_by_email(email)
    if not user or not verify_password(user["password"], password):
        return False, "Invalid credentials"

    return True, user