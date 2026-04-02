from celery import Celery
from config import REDIS_URL

# 创建Celery实例
celery_app = Celery(
    "worker",        # worker名称
    broker=REDIS_URL,  # 消息队列（任务发送）
    backend=REDIS_URL  # 结果存储
)