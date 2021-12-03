from src.models.libs.jwt import _revoke_tokens
from src.models.libs.security import verify_password, hash_password
from fastapi.responses import JSONResponse
from src.models.dbmodel.accounts_model import *
from src.models.libs.jwt import generatejwt, _refresh_token, HTTPException, AuthJWT
from datetime import datetime
from uuid import uuid4
import ast


class Authenticate(object):
    table: str = 'default'

    async def register(data: IRegister, db: Session):
        try:
            data.uid = data.uid if data.uid != None else f"{str(uuid4()).replace('-', '')}"

            auth_data = db.query(AuthModel).filter_by(email = data.email).first()
            db.close()

            if auth_data != None:
                return JSONResponse(status_code = 404, content = { "error":  "user found" } )

            if auth_data == None:
                auth = AuthModel(
                    uid = data.uid, 
                    email = data.email if data.email != None else '' , 
                    mobile = data.mobile if data.mobile != None else '' , 
                    password = hash_password(data.password) if data.password != None else '' , 
                    isVerified = data.isVerified if data.isVerified != None else False , 
                    auth_type = data.auth_type if data.auth_type != None else '' 
                )
                db.add(auth)
                db.commit()
                db.refresh(auth)

                tauth = TokensModel(
                    uid = data.uid, 
                    device = '', 
                    push_tokens = str([])
                )
                db.add(tauth)
                db.commit()
                db.refresh(tauth)

                user = AccountsModel(
                    uid = data.uid,
                    username = data.username if 'username' in data else '',
                    fullname = data.fullname if 'fullname' in data else '',
                    otherinfo = data.otherinfo if 'otherinfo' in data else '',
                    email = data.email if data.email != None else '' , 
                    phone = data.mobile if data.mobile != None else '' , 
                    sex = data.sex if 'sex' in data else '',
                    access = data.access if 'access' in data else 'user',
                    image = data.image if 'image' in data else '',
                    date_added = datetime.now(),
                    date_updated = datetime.now(),
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            db.close()
            # send verification email to account 

            return {
                "message": "user registered"
            }
        except Exception as ex:
            print(str(ex))
            return JSONResponse(status_code = 500, content = { "error":  str(ex) } )

    async def login(data: dict, db: Session, Authorize: AuthJWT):
        try:
            auth_data = None
            if data.auth_type == 'email':
                auth_data = db.query(AuthModel).filter_by(email = data.email).first()
            if data.auth_type == 'phone':
                auth_data = db.query(AuthModel).filter_by(mobile = data.mobile).first()
            db.close()


            if auth_data == None:
                return JSONResponse(status_code = 404, content = { "error":  "user not found" } )

            # if auth_data.isVerified == False or auth_data.isVerified == 0:
            #     return JSONResponse(status_code = 400, content = { "error":  "user account is not verified" } )

            check = verify_password(auth_data.password, data.password)
            if check == False:
                return JSONResponse(status_code = 401, content = { "error":  "password is incorrect" } )

            return generatejwt({
                    "uid": auth_data.uid
                }, Authorize)
        except Exception as ex:
            print(ex)
            return JSONResponse(status_code = 500, content = { "error": str(ex) } )

    async def social_auth(data: ISocialAuth, db: Session, Authorize: AuthJWT):
        try:
            if data.auth_type not in ['facebook', 'google']:
                return JSONResponse(status_code = 404, content = { "error":  "invalid social network" } )

            auth_data = db.query(AuthModel).filter_by(uid = data.uid).first()
            token_data = db.query(TokensModel).filter_by(uid = data.uid).first()
            account_data = db.query(AccountsModel).filter_by(uid = data.uid).first()
                
            if auth_data == None:
                auth = AuthModel(
                    uid = data.uid, 
                    email = data.email if data.email != None else '' , 
                    mobile = data.mobile if data.mobile != None else '' , 
                    password = hash_password(data.uid) , 
                    isVerified = data.isVerified if data.isVerified != None else False , 
                    auth_type = data.auth_type if data.auth_type != None else '' 
                )
                db.add(auth)
                db.commit()
                db.refresh(auth)

            if token_data == None:
                tauth = TokensModel(
                    uid = data.uid, 
                    device = '', 
                    push_tokens = str([])
                )
                db.add(tauth)
                db.commit()
                db.refresh(tauth)

            if account_data == None:
                user = AccountsModel(
                    uid = data.uid,
                    username = data.username if 'username' in data else '',
                    fullname = None,
                    otherinfo = '',
                    email = data.email if data.email != None else '' , 
                    phone = data.mobile if data.mobile != None else '' , 
                    sex = '',
                    access = data.access if 'access' in data else 'user',
                    image = data.image if 'image' in data else '',
                    date_added = datetime.now(),
                    date_updated = datetime.now(),
                )
                db.add(user)
                db.commit()
                db.refresh(user)

            db.close()

            return generatejwt({
                    "uid": data.uid
                }, Authorize)
        except Exception as ex:
            raise HTTPException(status_code = 500, detail=str(ex))

    async def reauthenticate_user(uid: str, db: Session, Authorize: AuthJWT):
        try:
            auth_data = db.query(AuthModel).filter_by(uid = uid).first()
            if auth_data is None:
                _revoke_tokens(Authorize)
                return JSONResponse(status_code = 404, content = { "error":  "User information not found"} )
                
            return _refresh_token(Authorize)
        except Exception as ex:
            raise HTTPException(status_code = 500, detail=str(ex))

    async def remove(uid: str, db: Session, Authorize: AuthJWT):
        try:
            auth_data = db.query(AuthModel).filter_by(uid = uid).first()
            if auth_data == None:
                return JSONResponse(status_code = 404, content = {
                    "error": "user not found"
                })

            token_data = db.query(TokensModel).filter_by(uid = uid).first()
            account_data = db.query(AccountsModel).filter_by(uid = uid).first()

            db.delete(auth_data)
            db.delete(token_data)
            db.delete(account_data)
            db.commit()
            db.close()

            return {
                "message": _revoke_tokens(Authorize)
            }
        except Exception as ex:
            return JSONResponse(status_code = 500, content = { "error": str(ex) } )

    async def logout(db: Session, Authorize: AuthJWT):
        try:
            return {
                "message": _revoke_tokens(Authorize)
            }
        except Exception as ex:
            return JSONResponse(status_code = 500, content = { "error": str(ex) } )

    async def confirm_user(token: str, db: Session):
        try:
            print(token)
            # auth_data = db.query(AuthModel).filter_by(uid = uid).first()

            # auth_data.isVerified = True

            # db.add(auth_data)
            # db.commit()
            # db.close()
            return {
                "message": "user verified"
            }
        except Exception as ex:
            return JSONResponse(status_code = 500, content = { "error": str(ex) } )





class Accounts(object):
    table: str = 'default'
    async def get_accounts(user_id: str, db: Session):
        try:
            print(user_id)
            if user_id != None:
                auth_data = db.query(AuthModel).filter_by(uid = user_id).all()
                token_data = db.query(TokensModel).filter_by(uid = user_id).all()
                user_data = db.query(AccountsModel).filter_by(uid = user_id).first()
                db.close()
                return user_data
            else:
                auth_data = db.query(AuthModel).all()
                token_data = db.query(TokensModel).all()
                user_data = db.query(AccountsModel).all()
                db.close()
                return user_data
            # if len(auth_data) > 0:
            #     for _user in auth_data:
            #         del(_user.password)
            #         del(_user.id)
            #         _user.tokens = 

        except Exception as ex:
            raise Exception(str(ex))

    async def delete_accounts(user_id: str, db: Session):
        try:
            pass
        except Exception as ex:
            raise Exception(str(ex))

    async def update_user_account(data: dict, db: Session):
        try:
            pass
        except Exception as ex:
            raise Exception(str(ex))


class Tokens(object):
    table: str = 'default'
    async def get_accounts_token(user_id: str, db: Session):
        try:
            tokens = db.query(TokensModel).all()
            db.close()
            return tokens
        except Exception as ex:
            raise Exception(str(ex))

    async def delete_accounts_token(user_id: str, db: Session):
        try:
            pass
        except Exception as ex:
            raise Exception(str(ex))

    async def update_user_account_token(data: ITokens, db: Session):
        try:
            tokens = db.query(TokensModel).filter_by(TokensModel.uid == data.uid).first()

            if tokens != None:
                tokens.push_tokens = str(data.push_tokens)
            else:
                sauth = TokensModel(uid = data.uid, device = data.device, push_tokens = str(data.push_tokens))
            db.add(sauth)
            db.commit()
            db.close()

            return {
                "message": "token saved"
            }
        except Exception as ex:
            raise Exception(str(ex))

