import bcrypt
def validict(data : dict):
    return {k: v for k, v in data.items() if v is not None}

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password