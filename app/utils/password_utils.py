import hashlib
import os
import base64
import hmac

# NIST recommended minimum (can increase later)
ITERATIONS = 310_000
SALT_SIZE = 16  # bytes

def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2-HMAC-SHA256
    Returns base64(salt + derived_key)
    """
    if not password:
        raise ValueError("Password cannot be empty")

    salt = os.urandom(SALT_SIZE)

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    return base64.b64encode(salt + dk).decode("utf-8")


def verify_password(stored_hash: str, password: str) -> bool:
    """
    Verify password against stored PBKDF2 hash
    """
    if not stored_hash or not password:
        return False

    decoded = base64.b64decode(stored_hash.encode("utf-8"))
    salt = decoded[:SALT_SIZE]
    stored_dk = decoded[SALT_SIZE:]

    new_dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    # Constant-time comparison (prevents timing attacks)
    return hmac.compare_digest(new_dk, stored_dk)
