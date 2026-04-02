import uuid, redis
from config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

class RedisLock:

    def __init__(self, key):
        self.key = key  
        self.value = str(uuid.uuid4()) 

    def acquire(self):
        return r.set(self.key, self.value, nx=True, ex=10)

    def release(self):
        lua = """
        if redis.call('get', KEYS[1]) == ARGV[1] then
            return redis.call('del', KEYS[1])
        else
            return 0
        end
        """
        r.eval(lua, 1, self.key, self.value)
