from sqlalchemy import Column, Integer, String
from db import Base

# 用户表模型（对应数据库users表）
class User(Base):
    __tablename__ = "users"  # 表名

    id = Column(Integer, primary_key=True, index=True)  # 主键
    username = Column(String, unique=True, index=True)  # 用户名（唯一）
    password = Column(String)  # 密码（存加密后的）
