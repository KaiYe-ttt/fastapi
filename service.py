from models import User
from utils import hash_password, verify_password

# 创建用户（业务逻辑层）
def create_user(db, username, password):
    # 查询数据库是否已存在（防重复注册）
    if db.query(User).filter(User.username == username).first():
        return None

    # 创建用户对象（密码加密存储）
    user = User(username=username, password=hash_password(password))

    db.add(user)      # 加入session
    db.commit()       # 提交事务
    db.refresh(user)  # 刷新获取数据库最新数据（比如id）

    return user

# 登录认证
def authenticate(db, username, password):
    # 查找用户
    user = db.query(User).filter(User.username == username).first()

    # 校验密码
    if user and verify_password(password, user.password):
        return user

    return None