from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import UserCreate, TaskRequest
from service import create_user, authenticate
from auth import create_token, verify_token
from tasks import long_task
from celery.result import AsyncResult
from celery_app import celery_app
from cache import get_cache, set_cache
from lock import RedisLock
from db import get_db

app = FastAPI()  # 创建FastAPI应用

security = HTTPBearer()

@app.post("/register")
def register(data: UserCreate, db=Depends(get_db)):

    user = create_user(db, data.username, data.password)

    if not user:
        raise HTTPException(400, "user exists")

    return {"id": user.id}

@app.post("/login")
def login(data: UserCreate, db=Depends(get_db)):

    user = authenticate(db, data.username, data.password)

    if not user:
        raise HTTPException(401)

    token = create_token({"user": user.username})

    return {"token": token}

# ================= 鉴权逻辑 =================

def get_user(c: HTTPAuthorizationCredentials = Depends(security)):

    payload = verify_token(c.credentials)  
    if not payload:
        raise HTTPException(401)

    return payload["user"] 

@app.post("/task")
def create_task(req: TaskRequest, user=Depends(get_user)):

    lock = RedisLock(f"lock:{user}")

    if not lock.acquire():
        raise HTTPException(429, "duplicate")

    try:
        task = long_task.delay(req.x, req.y)

        return {"task_id": task.id}

    finally:
        lock.release()

@app.get("/task/{task_id}")
def get_task(task_id: str, user=Depends(get_user)):

    cache_key = f"task:{task_id}"

    cached = get_cache(cache_key)

    if cached:
        return {"status": "cached", "result": cached}

    task = AsyncResult(task_id, app=celery_app)

    if task.status == "SUCCESS":
        set_cache(cache_key, task.result)

    return {"status": task.status, "result": task.result}
