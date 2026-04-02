import uuid, redis
from config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

# 分布式锁（解决并发问题）
class RedisLock:

    def __init__(self, key):
        self.key = key  # 锁的key
        self.value = str(uuid.uuid4())  # 唯一值（防误删）

    # 获取锁
    def acquire(self):
        # nx=True：只有key不存在才设置（保证互斥）
        # ex=10：10秒自动过期（防死锁）
        return r.set(self.key, self.value, nx=True, ex=10)

    # 释放锁（必须保证是自己的锁）
    def release(self):
        # Lua脚本保证原子性（避免误删别人的锁）
        lua = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """
        r.eval(lua, 1, self.key, self.value)