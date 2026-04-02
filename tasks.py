from celery_app import celery_app
import time

# 定义异步任务
# bind=True：允许访问self（用于更新状态）
# autoretry_for：异常自动重试
# retry_backoff：指数退避
# max_retries：最大重试次数
@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def long_task(self, x, y):

    # 模拟耗时任务
    for i in range(5):
        time.sleep(1)

        # 更新任务进度
        self.update_state(state="PROGRESS", meta={"progress": i})

    return x + y  # 返回结果