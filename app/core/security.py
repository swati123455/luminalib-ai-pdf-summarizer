from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import get_settings
from fastapi.security import OAuth2PasswordBearer

oauth_2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password:str, hash: str) -> bool:
    return pwd_context.verify(password, hash)

def create_access_token(data:dict):
    print("\n--- TOKEN DEBUG ---")
    print("SECRET:", settings.jwt_secret)
    print("ALGO:", settings.jwt_algorithm)
    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    print("TOKEN CREATED:", token)

    return token
