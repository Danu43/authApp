from ..extensions.mongo import get_db

def get_user_by_email(email):
    if not email:
        return None
    return get_db().users.find_one({"email": email.lower()})


def create_user(user_data):
    return get_db().users.insert_one(user_data)