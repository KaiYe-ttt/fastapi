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

# HTTP Bearer认证（Authorization: Bearer xxx）
security = HTTPBearer()

# ================= 注册接口 =================
@app.post("/register")
def register(data: UserCreate, db=Depends(get_db)):

    # 调用业务层
    user = create_user(db, data.username, data.password)

    if not user:
        raise HTTPException(400, "user exists")

    return {"id": user.id}

# ================= 登录接口 =================
@app.post("/login")
def login(data: UserCreate, db=Depends(get_db)):

    user = authenticate(db, data.username, data.password)

    if not user:
        raise HTTPException(401)

    # 生成token
    token = create_token({"user": user.username})

    return {"token": token}

# ================= 鉴权逻辑 =================

def get_user(c: HTTPAuthorizationCredentials = Depends(security)):

    payload = verify_token(c.credentials)  # 解析token

    if not payload:
        raise HTTPException(401)

    return payload["user"]  # 返回用户名

# ================= 提交任务 =================
@app.post("/task")
def create_task(req: TaskRequest, user=Depends(get_user)):

    # 创建用户级别锁（防重复提交）
    lock = RedisLock(f"lock:{user}")

    # 获取锁失败 -> 说明重复请求
    if not lock.acquire():
        raise HTTPException(429, "duplicate")

    try:
        # 发送异步任务
        task = long_task.delay(req.x, req.y)

        return {"task_id": task.id}

    finally:
        # 一定要释放锁
        lock.release()

# ================= 查询任务 =================
@app.get("/task/{task_id}")
def get_task(task_id: str, user=Depends(get_user)):

    cache_key = f"task:{task_id}"

    # 先查缓存（减少压力）
    cached = get_cache(cache_key)

    if cached:
        return {"status": "cached", "result": cached}

    # 查询Celery任务状态
    task = AsyncResult(task_id, app=celery_app)

    # 如果完成 -> 写入缓存
    if task.status == "SUCCESS":
        set_cache(cache_key, task.result)

    return {"status": task.status, "result": task.result}
