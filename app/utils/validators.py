import re

EMAIL_REGEX = r"^[^@]+@[^@]+\.[^@]+$"

def validate_email(email: str):
    if not email:
        return False, "Email is required"

    email = email.strip().lower()

    if not re.match(EMAIL_REGEX, email):
        return False, "Invalid email format"

    return True, email


def validate_password(password: str):
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    return True, None


def validate_name(name: str):
    if not name:
        return False, "Name is required"

    if not name.replace(" ", "").isalpha():
        return False, "Name must contain only letters"

    return True, name.strip().title()
