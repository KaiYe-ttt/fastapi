from jose import jwt
from datetime import datetime
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

# 生成JWT Token
# data一般是用户信息
# exp是过期时间（标准字段）
def create_token(data: dict):
    to_encode = data.copy()  # 防止修改原数据

    # 添加过期时间
    to_encode.update({"exp": datetime.utcnow() + ACCESS_TOKEN_EXPIRE})

    # 生成token
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 校验token
# 成功返回payload（用户信息）
# 失败返回None
def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None