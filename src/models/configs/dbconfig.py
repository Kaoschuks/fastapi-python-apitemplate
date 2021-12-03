from src.models.core import os, logger, app, Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
import sqlalchemy
from sqlalchemy.orm import sessionmaker

mode = os.getenv("DEBUG")
baseDir = os.path.abspath(os.path.dirname(__file__))

uri = os.getenv("SQLALCHEMY_DATABASE_URI")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
server = os.getenv("DB_SERVER")
port = os.getenv("DB_PORT")
db = os.getenv("DB_NAME")
SQLALCHEMY_DATABASE_URL = 'sqlite:///' + os.path.join(baseDir, f"{db}.db")

if mode == False:
    SQLALCHEMY_DATABASE_URL = f"{uri}://{username}:{password}@{server}:{port}/{db}" 

# print(SQLALCHEMY_DATABASE_URL)
Base: DeclarativeMeta = declarative_base()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args = {
        'check_same_thread': False
    }, 
    # echo = True,
    convert_unicode = True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
