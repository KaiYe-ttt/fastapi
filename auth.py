from jose import jwt
from datetime import datetime
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE


def create_token(data: dict):
    to_encode = data.copy()  


    to_encode.update({"exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE})


    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None
