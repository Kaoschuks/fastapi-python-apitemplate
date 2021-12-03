from pydantic import BaseModel
from src.models.configs.dbconfig import Base, engine, get_db, Depends
from sqlalchemy import exc, and_, or_, Column, Integer, String, BigInteger, Text, String, Boolean
from sqlalchemy.types import Date
from datetime import date
from sqlalchemy.orm import Session


class IMail(BaseModel):
    email: str
    subject: str
    message: str
    sender: str

    class Config:
        orm_mode = True