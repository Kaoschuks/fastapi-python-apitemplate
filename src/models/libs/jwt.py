from sqlalchemy.sql.functions import user
from src.models.core import app, os
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from datetime import timedelta

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET_KEY")
    authjwt_denylist_enabled: bool = bool(os.getenv("JWT_DENY_ENABLED"))
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    # authjwt_token_location: set = {"cookies"}
    access_expires: int = timedelta(days = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE")))
    refresh_expires: int = timedelta(days = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE")))
    authjwt_algorithm: str = str(os.getenv("JWT_ACCESS_ALGORITHM"))
    authjwt_public_key: str = os.getenv("JWT_PUBLIC_KEY")
    authjwt_private_key: str = os.getenv("JWT_PRIVATE_KEY")

denylist = set()

@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in denylist

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    print(str(exc))
    raise JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc)}
    )

def validate_token(Authorize: AuthJWT, type: str = 'access'):
    try:  
        Authorize.jwt_refresh_token_required() if type == 'refresh' else Authorize.jwt_required()
        userinfo = Authorize.get_jwt_subject()
        return userinfo
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e) if str(e) != '' else "access forbidden and denied")

def generatejwt(user: dict, Authorize: AuthJWT):
    try:  
        return { 
            "access_token": Authorize.create_access_token(
                subject = str(user['uid']), 
                fresh = True, 
                expires_time = timedelta(days = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE")))
            ),
            "refresh_token": Authorize.create_refresh_token(subject = str(user['uid']))
        }
    except Exception as e:
        raise Exception(str(e))

def _refresh_token(Authorize: AuthJWT):
    try:  
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        return { 
            "token": Authorize.create_access_token(subject = current_user),
            "refresh_token": Authorize.create_refresh_token(subject = current_user)
        }
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code = 500, detail=str(e))
        
def _revoke_tokens(Authorize: AuthJWT):
    try:  
        Authorize.jwt_required()
        # Authorize.jwt_refresh_token_required()

        jti = Authorize.get_raw_jwt()['jti']
        denylist.add(jti)
        return "authorization revoked and deleted"
    except Exception as e:
        raise Exception(str(e))
