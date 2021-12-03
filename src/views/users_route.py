from src.models.core import app, Depends
from src.controllers.accounts import *
from src.controllers.reviews import *
from fastapi import APIRouter
from src.models.libs.jwt import AuthJWT, validate_token

reviews_router = APIRouter(route_class = Reviews)

@app.post('/login', tags = ['Authentication'])
async def login(form_data: IAuth, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Authenticate.login(form_data, db, Authorize)

@app.post('/register', tags = ['Authentication'])
async def register(form_data: IRegister, db: Session = Depends(get_db)):
    return await Authenticate.register(form_data, db)

@app.post('/socialauth', tags = ['Authentication'])
async def social_login(form_data: ISocialAuth, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Authenticate.social_auth(form_data, db, Authorize)

@app.get('/confirm/{token}', tags = ['Authentication'])
async def verify_user(token: str, db: Session = Depends(get_db)):
    return await Authenticate.confirm_user(token, db)

@app.put('/recover', tags = ['Authentication'])
async def recover(form_data: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass

@app.put('/refreshtoken', tags = ['Authentication'])
async def refresh_token(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Authenticate.reauthenticate_user(validate_token(Authorize, 'refresh'), db, Authorize)

@app.delete('/remove', tags = ['Authentication'])
async def delete(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Authenticate.remove(validate_token(Authorize), db, Authorize)

@app.delete('/logout', tags = ['Authentication'])
async def logged_out(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Authenticate.logout(db, Authorize)




@app.get('/user', tags = ['User Profile'], operation_id="authorize")
async def get_profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    return await Accounts.get_accounts(validate_token(Authorize), db)

@app.put('/user', tags = ['User Profile'], operation_id="authorize")
async def get_profile(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    uid = validate_token(Authorize)
    pass




@app.get('/users', tags = ['Users Management'], operation_id="authorize")
async def get_all_accounts(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    validate_token(Authorize)
    return await Accounts.get_accounts(None, db)

@app.get('/users/<userid>', tags = ['Users Management'], operation_id="authorize")
async def get_account_by_id(userid: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    validate_token(Authorize)
    return await Accounts.get_accounts(userid, db)

@app.put('/users/<userid>', tags = ['Users Management'], operation_id="authorize")
async def update_account(formdata: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    validate_token(Authorize)
    return await Accounts.update_user_account(formdata, db)




@app.get('/businesses', tags = ['Business Management'], operation_id="authorize")
async def get_all_businesses_info(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    pass

@app.get('/businesses/<businessid>', tags = ['Business Management'], operation_id="authorize")
async def get_company_info(businessid: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    pass

@app.put('/businesses/<businessid>', tags = ['Business Management'], operation_id="authorize")
async def update_company_info(businessid: str, formdata: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    pass

@app.delete('/businesses/<businessid>', tags = ['Business Management'], operation_id="authorize")
async def delete_company_info(businessid: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    pass




# @app.get('/tokens/<userid>', tags = ['Push Management'], operation_id="authorize")
# async def get_accounts_tokens(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     validate_token(Authorize)
#     return await Tokens.get_accounts_token(None, db)

# @app.put('/tokens/<userid>', tags = ['Push Management'], operation_id="authorize")
# async def update_accounts_tokens(data: ITokens, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     validate_token(Authorize)
#     return await Tokens.update_accounts_token(data, db)



@app.post('/activities', tags = ['User Activities'], operation_id="authorize")
async def save_user_activity(activity_data: dict, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass

@app.get('/activities', tags = ['User Activities'], operation_id="authorize")
async def get_user_activity(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    pass



@reviews_router.post("/", operation_id="authorize")
async def save_user_review(data: IReviews, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    data.ads_id = uid
    return await Reviews.add_reviews(data, db)

@reviews_router.put("/{review_id}", operation_id="authorize")
async def save_user_review(review_id: str, data: IReviews, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    data.ads_id = uid
    return await Reviews.update_reviews(data, db)


app.include_router(reviews_router, prefix="/users/reviews", tags = ['Users Reviews'])