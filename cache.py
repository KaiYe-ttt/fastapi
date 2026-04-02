import redis, json
from config import REDIS_URL

# 创建Redis客户端
r = redis.Redis.from_url(REDIS_URL)

# 设置缓存
# key: 缓存key
# value: 任意Python对象（转JSON存储）
# ex: 过期时间（秒）
def set_cache(key, value, ex=60):
    r.set(key, json.dumps(value), ex=ex)

# 获取缓存
def get_cache(key):
    v = r.get(key)  # 从Redis读取

    # 如果存在则反序列化JSON
    return json.loads(v) if v else None