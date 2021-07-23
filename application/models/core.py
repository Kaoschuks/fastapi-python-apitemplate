from fastapi import FastAPI, HTTPException, Depends, Request, status, WebSocket, WebSocketDisconnect, Query
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
import random
import os
import sys
from dotenv import load_dotenv
import threading as threading
import requests as req
import logging as logger
load_dotenv()
logger.basicConfig(level = logger.DEBUG, stream = sys.stdout)

app = FastAPI(
    title = os.getenv("APP_NAME"),
    description = os.getenv("APP_DESCRIPTION")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = os.getenv("APP_NAME"),
        description = os.getenv("APP_DESCRIPTION"),
        version =  os.getenv("APP_VERSION"),
        routes=app.routes,
    )

    # Custom documentation fastapi-jwt-auth
    headers = {
        "name": "Authorization",
        "in": "header",
        "required": True,
        "schema": {
            "title": "Authorization",
            "type": "string"
        },
    }

    # Get routes from index 4 because before that fastapi define router for /openapi.json, /redoc, /docs, etc
    # Get all router where operation_id is authorize
    router_authorize = [route for route in app.routes[4:] if route.operation_id == "authorize"]

    for route in router_authorize:
        method = list(route.methods)[0].lower()
        try:
            # If the router has another parameter
            openapi_schema["paths"][route.path][method]['parameters'].append(headers)
        except Exception:
            # If the router doesn't have a parameter
            openapi_schema["paths"][route.path][method].update({"parameters":[headers]})

    app.openapi_schema = openapi_schema
    return app.openapi_schema
