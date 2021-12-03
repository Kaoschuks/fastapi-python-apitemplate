from typing import Any, Optional
from pydantic import BaseModel
from src.models.configs.dbconfig import Base, engine, get_db, Depends
from sqlalchemy import exc, and_, or_, Column, Integer, String, BigInteger, Text, String, Boolean
from sqlalchemy.types import Date
from datetime import date
from sqlalchemy.orm import Session


class IRegister(BaseModel):
    uid: Optional[str] = None
    email: Optional[str]
    mobile: Optional[str] = None
    password: Optional[str] = None
    auth_type: Optional[str] = 'email'
    username: Optional[str]
    fullname: Optional[str]
    otherinfo: Optional[Any]
    image: Optional[str]
    sex: Optional[str]
    access: str = 'user'
    isVerified: Optional[bool] = False

class ISocialAuth(BaseModel):
    auth_type: Optional[str] = 'facebook'
    uid: str = None
    username: Optional[str] = None
    email: Optional[str]
    image: Optional[str]
    access: str = 'user'
    mobile: Optional[str] = None
    isVerified: Optional[bool] = False

class IAuth(BaseModel):
    auth_type: Optional[str] = 'email'
    uid: Optional[str] = None
    email: Optional[str]
    mobile: Optional[str] = None
    password: Optional[str] = None
    isVerified: Optional[bool] = False

    class Config:
        orm_mode = True

class ITokens(BaseModel):
    uid: str
    device: str
    push_tokens: str

    class Config:
        orm_mode = True


class IAccount(BaseModel):
    uid: str
    username: Optional[str]
    email: Optional[str]
    image: Optional[str]
    fullname: Optional[str]
    otherinfo: Optional[Any]
    phone: Optional[str]
    sex: Optional[str]
    access: str
    date_added: Optional[str]
    date_updated: Optional[str]

    class Config:
        orm_mode = True

class AuthModel(Base):
    __tablename__ = "auth"

    id = Column(Integer, primary_key = True)
    uid = Column(String(100), unique = True)
    email = Column(String(100))
    mobile = Column(String(50))
    password = Column(String(200))
    isVerified = Column(Integer)
    auth_type = Column(String(50))


class TokensModel(Base):
    __tablename__ = "tokens"
    
    id = Column(Integer, primary_key = True)
    uid = Column(String(100), unique = True)
    device = Column(String(100))
    push_tokens = Column(Text())


class AccountsModel(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key = True)
    uid = Column(String(100), unique = True)
    username = Column(String(100))
    fullname = Column(Text())
    otherinfo = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    sex = Column(String(7))
    access = Column(String(7))
    image = Column(Text())
    date_added = Column(String(50))
    date_updated = Column(String(50))