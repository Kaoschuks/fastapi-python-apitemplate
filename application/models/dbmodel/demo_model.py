from pydantic import BaseModel
from application.models.configs.dbconfig import Base, engine, get_db, Depends
from sqlalchemy import exc, and_, or_, Column, Integer, String, BigInteger, Text, String, Boolean
from sqlalchemy.types import Date
from datetime import date
from sqlalchemy.orm import Session


class ILogin(BaseModel):
    username: str
    password: str

class IRecord(BaseModel):
    id: int
    date: date
    country: str
    cases: int
    deaths: int
    recoveries: int

    class Config:
        orm_mode = True

class Record(Base):
    __tablename__ = "Records"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    country = Column(String(255), index=True)
    cases = Column(Integer)
    deaths = Column(Integer)
    recoveries = Column(Integer)

Base.metadata.create_all(bind=engine)