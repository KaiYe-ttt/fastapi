from sqlalchemy import create_engine  # 创建数据库引擎
from sqlalchemy.orm import sessionmaker, declarative_base  # session工厂 + ORM基类

# 创建数据库引擎（这里用sqlite，面试可以说可替换MySQL/PostgreSQL）
engine = create_engine(
    "sqlite:///./test.db",  # 数据库文件路径
    connect_args={"check_same_thread": False}  # sqlite多线程支持
)

# 创建Session工厂（每个请求使用一个session）
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ORM基类（所有模型继承它）
Base = declarative_base()

# FastAPI依赖注入：自动管理数据库连接生命周期
# 每个请求进来：创建session
# 请求结束：关闭session（防止连接泄漏）
def get_db():
    db = SessionLocal()  # 创建数据库连接
    try:
        yield db  # 返回给接口使用
    finally:
        db.close()  # 请求结束关闭连接