from application.models.core import os, logger, app, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib
import binascii

if os.getenv("DEBUG") is False:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    print(SQLALCHEMY_DATABASE_URI)
else:
    baseDir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(baseDir, 'app.db')

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, convert_unicode=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
logger.debug(f"database connection started {SQLALCHEMY_DATABASE_URL}")

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
