from src.models.configs.dbconfig import *
from sqlalchemy import exc, and_, or_, Column, Integer, String, BigInteger, Text, String, Boolean, Table
from sqlalchemy.types import Date
from datetime import date
from pydantic import BaseModel
from typing import Any, Optional
from sqlalchemy.orm import Session

class IChargeOrder(BaseModel):
    transid: Optional[str]
    orderid: Optional[str]
    uid: str
    email: str
    payment_source: str
    summary: str
    amount: int
    charge_type: str
    authcode: str
    country: Optional[str]
    date_added: Optional[date]
    date_updated: Optional[date]

    class Config:
        orm_mode = True

class ITransOrder(BaseModel):
    orderid: Optional[str]
    uid: Optional[str]
    summary: Optional[str]
    order_type: str
    payment_gateway: Optional[str]
    total_amount: int
    status: Optional[bool]
    date_added: Optional[date]
    date_updated: Optional[date]

    class Config:
        orm_mode = True

class IRecipient(BaseModel):
    type: Optional[str] = 'balance'
    name: str
    account_number: str
    bank_code: str
    currency: Optional[str] = 'NGN'

class ITransfer(BaseModel):
    uid: str
    walletid: str
    payment_source: str
    status: str
    summary: Optional[str]
    amount: int
    recipient: IRecipient

    class Config:
        orm_mode = True

class ITransactions(BaseModel):
    orderid: Optional[str]
    transid: Optional[str]
    uid: str
    summary: str
    amount: int
    status: Optional[str]
    type: Optional[str]
    transaction_info: Optional[Any]
    date_added: Optional[date]
    date_updated: Optional[date]

    class Config:
        orm_mode = True




class OrdersModel(Base):
    __tablename__ = f"orders"

    id = Column(Integer, primary_key = True, index=True)
    orderid = Column(String(50), unique = True)
    order_type = Column(String(50))
    payment_gateway = Column(String(50))
    uid = Column(String(50))
    total_amount = Column(String(50))
    summary = Column(Text())
    status = Column(Boolean)
    date_updated = Column(Date)
    date_added = Column(Date)


class TransactionsModel(Base):
    __tablename__ = f"transactions"

    id = Column(Integer, primary_key = True, index=True)
    orderid = Column(String(50))
    transid = Column(String(50), unique = True)
    uid = Column(String(50))
    transaction_info = Column(Text())
    amount = Column(String(50), nullable=False, default=0)
    summary = Column(Text())
    status = Column(String(50), nullable=False, default=True)
    type = Column(String(50))
    date_updated = Column(Date)
    date_added = Column(Date)