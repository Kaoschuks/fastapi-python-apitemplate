from src.controllers.orders import Orders, ITransOrder, Optional
from src.models.core import app, Depends
from src.models.configs.dbconfig  import get_db
from sqlalchemy.orm import Session
from fastapi import Request
from src.models.libs.jwt import AuthJWT, validate_token

@app.post('/orders', tags = ['Orders'])
async def save_order(data: ITransOrder, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await Orders.save_order(data, uid, db)

@app.put('/orders/{orderid}', tags = ['Orders'])
async def update_an_order(orderid: str, data: ITransOrder, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await Orders.update_order(orderid, data, db)

@app.get('/orders', tags = ['Orders'])
async def get_orders(request: Request, limit: Optional[int] = 100, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await Orders.get_orders(None, uid, db, limit)

@app.get('/orders/all', tags = ['Orders'])
async def get_all_orders(request: Request, limit: Optional[int] = 100, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    return await Orders.get_orders(None, None, db, limit)

@app.get('/orders/{orderid}', tags = ['Orders'])
async def get_an_orders(orderid: str, request: Request, limit: Optional[int] = 100, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await Orders.get_orders(orderid, uid, db, limit)

# @app.get('/transactions/verify/{transid}', tags = ['Transactions'])
# async def verifytransactions(transid: str, db: Session = Depends(get_db)):
#     return await Transactions.verify(transid, db)