from fastapi import FastAPI
import os, sys, uvicorn
from dotenv import load_dotenv
import logging as logger

load_dotenv()
logger.basicConfig(level = logger.DEBUG, stream = sys.stdout)
logger.getLogger("aiomysql").setLevel(logger.ERROR)
logger.getLogger("aiosqlite").setLevel(logger.ERROR)
logger.getLogger("httpcore").setLevel(logger.ERROR)
logger.getLogger("httpx").setLevel(logger.ERROR)

app = FastAPI(
    # lifespan = lifespan,
    title = os.getenv("APP_NAME"),
    description = os.getenv("APP_DESCRIPTION"),
    version = os.getenv("APP_VERSION")
)


class UnicornException(Exception):
    def __init__(self, code: int, error: str):
        self.code = code
        self.error = error
