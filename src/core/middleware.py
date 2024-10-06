from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from src.utils.libs import SecurityHeadersMiddleware
from src.core.config import app
import os, ssl, ast

origins = ast.literal_eval(os.getenv("APP_ORIGINS"))

app.add_middleware( 
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

app.add_middleware(
    GZipMiddleware, minimum_size=10
)

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=origins
)

app.add_middleware(
    SecurityHeadersMiddleware, csp=True
)

if os.getenv("SSL") is True:
    app.add_middleware(HTTPSRedirectMiddleware)

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context


Instrumentator().instrument(app).expose(app)