from datetime import timedelta 

REDIS_URL = "redis://localhost:6379/0"  
SECRET_KEY = "secret"  
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE = timedelta(hours=1) 
