from datetime import timedelta  # timedelta用于定义时间间隔（比如token过期时间）

REDIS_URL = "redis://localhost:6379/0"  # Redis连接地址（缓存 + 分布式锁 + Celery broker）
SECRET_KEY = "secret"  # JWT签名密钥（生产环境必须用复杂字符串）
ALGORITHM = "HS256"  # JWT加密算法
ACCESS_TOKEN_EXPIRE = timedelta(hours=1)  # token过期时间：1小时