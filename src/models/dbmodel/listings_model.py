from typing import Any, Optional

from sqlalchemy.sql.schema import ForeignKey
from pydantic import BaseModel
from src.models.configs.dbconfig import Base, engine, get_db, Depends
from sqlalchemy import exc, and_, or_, Column, Integer, String, BigInteger, Text, String, Boolean
from sqlalchemy.types import Date
from datetime import date
from sqlalchemy.orm import Session, relationship


class ICategory(BaseModel):
    name: str
    summary: str
    image: str
    subcategory: str
    parent: str

    class Config:
        orm_mode = True


class IReviews(BaseModel):
    ads_id: str
    comments: str
    likes: str
    saved: str
    dislike: str

    class Config:
        orm_mode = True


class IAdsModel(BaseModel):
    ads_id: Optional[str] = None
    uid: Optional[str] = None
    name: str
    price: str = 0.00
    description: str
    images: Any
    category: str
    brands: Optional[str] = None
    tags: Optional[Any]
    isFeatured: Optional[bool] = False
    featuredName: Optional[str] = None
    is_commentable: Optional[bool] = True
    date_added: Optional[str] = None
    date_updated: Optional[str] = None
    reviewInfo: Optional[Any]

    class Config:
        orm_mode = True





class CategoriesModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key = True)
    name = Column(String(50))
    subcategory = Column(String(5))
    parent = Column(String(50))
    summary = Column(Text())
    image = Column(Text())



class AdsModel(Base):
    __tablename__ = "adslistings"

    id = Column(Integer, primary_key = True)
    uid = Column(String(100))
    ads_id = Column(String(100), unique = True)
    name = Column(String(50))
    price = Column(String(10))
    description = Column(Text())
    images = Column(Text())
    category = Column(String(50))
    brands = Column(String(50))
    tags = Column(String(100))
    isFeatured = Column(Boolean())
    featuredName = Column(String(20))
    is_commentable = Column(Boolean())
    date_added = Column(String(50))
    date_updated = Column(String(50))
    reviewInfo = relationship('ReviewModel', backref="adslistings", uselist=False)
    


class ReviewModel(Base):
    __tablename__ = "reviewslistings"

    id = Column(Integer, primary_key = True)
    ads_id = Column(BigInteger, ForeignKey('adslistings.ads_id'), unique = True)
    comments = Column(Text())
    likes = Column(Text())
    saved = Column(Text())
    dislike = Column(Text())