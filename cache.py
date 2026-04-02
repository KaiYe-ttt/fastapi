import redis, json
from config import REDIS_URL

r = redis.Redis.from_url(REDIS_URL)

def set_cache(key, value, ex=60):
    r.set(key, json.dumps(value), ex=ex)

def get_cache(key):
    v = r.get(key) 

    return json.loads(v) if v else None
