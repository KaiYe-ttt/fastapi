from celery import Celery
from config import REDIS_URL

# 创建Celery实例
celery_app = Celery(
    "worker",       
    broker=REDIS_URL, 
    backend=REDIS_URL  
)
