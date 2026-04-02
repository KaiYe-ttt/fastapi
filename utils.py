import bcrypt

def hash_password(pwd: str):

    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def verify_password(pwd: str, hashed: str):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())
