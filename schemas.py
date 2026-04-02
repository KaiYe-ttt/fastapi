from pydantic import BaseModel

# 注册/登录请求体
class UserCreate(BaseModel):
    username: str
    password: str

# 异步任务请求体
class TaskRequest(BaseModel):
    x: int
    y: int