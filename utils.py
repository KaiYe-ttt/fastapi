import bcrypt

# 密码加密（不可逆）
def hash_password(pwd: str):
    # encode：字符串转字节
    # gensalt：生成随机盐（防止彩虹表攻击）
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

# 校验密码
# 用户输入的pwd vs 数据库中的hashed
# 返回True/False
def verify_password(pwd: str, hashed: str):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())