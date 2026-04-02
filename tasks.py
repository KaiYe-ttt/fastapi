from celery_app import celery_app
import time

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def long_task(self, x, y):

    for i in range(5):
        time.sleep(1)

        self.update_state(state="PROGRESS", meta={"progress": i})

    return x + y 
