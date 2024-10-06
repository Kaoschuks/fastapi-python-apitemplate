from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from src.core.config import app, os
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from redis import asyncio as aioredis
from fastapi_async_sqlalchemy import db

baseDir = os.path.abspath(os.path.dirname(__file__))
uri = os.getenv("SQLALCHEMY_DATABASE_URI")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
server = os.getenv("DB_SERVER")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")
mode = os.getenv("DEBUG")

if mode == 'false':
    SQLALCHEMY_DATABASE_URL = f"{uri}://{username}:{password}@{server}:{port}/{dbname}" 
else:
    baseDir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///' + os.path.join(baseDir, f'{dbname}.db')

Base: DeclarativeMeta = declarative_base()
engine = create_async_engine( SQLALCHEMY_DATABASE_URL,  connect_args = {
        'check_same_thread': False
    } if mode == "true" else {} )

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url = SQLALCHEMY_DATABASE_URL,
    # engine_args = {              
    #     "pool_pre_ping": True, # feature will normally emit SQL equivalent to “SELECT 1” each time a connection is checked out from the pool
    #     "pool_size": 10,        # number of connections to keep open at a time
    #     "max_overflow": 100,    # number of connections to allow to be opened above pool_size
    # } if mode == "true" else {
    #     # "echo": True
    # } 
)

redis = aioredis.from_url(os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True)