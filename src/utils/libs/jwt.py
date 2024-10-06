# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from urllib.parse import quote_plus
# from pydantic_settings import BaseSettings

# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

# class Settings(BaseSettings):
    
#     # Database
#     DB_USER: str = os.getenv('MYSQL_USER')
#     DB_PASSWORD: str = os.getenv('MYSQL_PASSWORD')
#     DB_NAME: str = os.getenv('MYSQL_DB')
#     DB_HOST: str = os.getenv('MYSQL_SERVER')
#     DB_PORT: str = os.getenv('MYSQL_PORT')
#     DATABASE_URL: str = f"mysql+pymysql://{DB_USER}:%s@{DB_HOST}:{DB_PORT}/{DB_NAME}" % quote_plus(DB_PASSWORD)
    
#     # JWT 
#     JWT_SECRET: str = os.getenv('JWT_SECRET', '709d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7')
#     JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM', "HS256")
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('JWT_TOKEN_EXPIRE_MINUTES', 60)
    
# def get_settings() -> Settings:
#     return Settings()

# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer
# from starlette.authentication import AuthCredentials, UnauthenticatedUser
# from datetime import timedelta, datetime
# from jose import jwt, JWTError
# from core.config import get_settings
# from fastapi import Depends

# settings = get_settings()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# async def create_access_token(data,  expiry: timedelta):
#     payload = data.copy()
#     expire_in = datetime.utcnow() + expiry
#     payload.update({"exp": expire_in})
#     return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

# async def create_refresh_token(data):
#     return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


# def get_token_payload(token):
#     try:
#         payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
#     except JWTError:
#         return None
#     return payload


# def get_current_user(token: str = Depends(oauth2_scheme), db = None):
#     payload = get_token_payload(token)
#     if not payload or type(payload) is not dict:
#         return None

#     user_id = payload.get('id', None)
#     if not user_id:
#         return None

#     user = db.query(UserModel).filter(UserModel.id == user_id).first()
#     return user


# class JWTAuth:
    
#     async def authenticate(self, conn):
#         guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        
#         if 'authorization' not in conn.headers:
#             return guest
        
#         token = conn.headers.get('authorization').split(' ')[1]  # Bearer token_hash
#         if not token:
#             return guest
        
#         user = get_current_user(token=token)
        
#         if not user:
#             return guest
        
#         return AuthCredentials('authenticated'), user