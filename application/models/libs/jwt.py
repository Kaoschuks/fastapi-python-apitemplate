from application.models.core import app, WebSocket, os, Query
from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel
from datetime import timedelta

class Settings(BaseModel):
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_samesite: str = 'lax'
    authjwt_cookie_secure: bool = True
    authjwt_cookie_csrf_protect: bool = False
    authjwt_secret_key: str = os.getenv("SECRET_KEY")
    authjwt_denylist_enabled: bool = bool(os.getenv("JWT_DENY_ENABLED"))
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: int = timedelta(days = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE")))
    refresh_expires: int = timedelta(days = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE")))
    # authjwt_algorithm: str = str(os.getenv("JWT_ACCESS_ALGORITHM"))
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
    raise JSONResponse(
        status_code=exc.status_code,
        detail={"details": str(exc)}
    )

def validate_token(Authorize: AuthJWT):
    try:  
        Authorize.jwt_required()
        userinfo = Authorize.get_jwt_subject()
        return userinfo
    except AuthJWTException as a_err:
        raise HTTPException(
            status_code = 403,
            detail = str(a_err) if str(a_err) != '' else "Access forbidden. Authorization required"
        )
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e) if str(e) != '' else "Internal service error")

async def websocket_validate_token(websocket: WebSocket, Authorize: AuthJWT, token: str = Query(...)):
    try:  
        Authorize.jwt_required("websocket", token = token)
        userinfo = Authorize.get_raw_jwt(token)
        return userinfo
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()

def generatejwt(user: dict, Authorize: AuthJWT):
    try:  
        resp = { 
            "access_token": Authorize.create_access_token(
                subject = str(user['uid']), 
                fresh = True, 
                algorithm = str(os.getenv("JWT_ACCESS_ALGORITHM")),
                expires_time = timedelta(days = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE")))
            ),
            "refresh_token": Authorize.create_refresh_token(subject = str(user['uid']), algorithm = str(os.getenv("JWT_REFRESH_ALGORITHM")))
        }
        Authorize.set_access_cookies(resp['access_token'])
        Authorize.set_refresh_cookies(resp['refresh_token'])
        return resp
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

def _refresh_token(Authorize: AuthJWT):
    try:  
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        resp = { 
            "token": Authorize.create_access_token(subject = current_user),
            "refresh_token": Authorize.create_refresh_token(subject = current_user)
        }
        Authorize.set_access_cookies(resp['token'])
        return resp
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
        
def _revoke_tokens(Authorize: AuthJWT):
    try:  
        Authorize.jwt_required()
        Authorize.jwt_refresh_token_required()
        Authorize.unset_jwt_cookies()

        jti = Authorize.get_raw_jwt()['jti']
        denylist.add(jti)
        raise HTTPException(status_code = 403, detail="All tokens has been revoke")
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
