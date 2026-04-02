from models import User
from utils import hash_password, verify_password

def create_user(db, username, password):
    if db.query(User).filter(User.username == username).first():
        return None

    user = User(username=username, password=hash_password(password))

    db.add(user)    
    db.commit()      
    db.refresh(user)  

    return user

def authenticate(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if user and verify_password(password, user.password):
        return user

    return None
