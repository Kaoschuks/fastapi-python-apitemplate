from src.models.dbmodel.payment_model import ITransfer
from src.controllers.orders import Transactions, ITransactions, Optional, IChargeOrder
from src.models.core import app, Depends
from src.models.configs.dbconfig  import get_db
from sqlalchemy.orm import Session
from fastapi import Request

@app.post('/transactions', tags = ['Transactions'])
async def save_transactions(data: ITransactions, request: Request, db: Session = Depends(get_db)):
    return await Transactions.save_transactions(data, data.uid, db)

@app.get('/transactions/all', tags = ['Transactions'])
async def get_all_transactions(request: Request, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    return await Transactions.get_transactions(None, None, db, limit)

@app.get('/transactions', tags = ['Transactions'])
async def get_user_transactions(request: Request, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    return await Transactions.get_transactions(None, request.headers['uid'], db, limit)

@app.get('/transactions/{transid}', tags = ['Transactions'])
async def get_a_transactions(transid: str, request: Request, db: Session = Depends(get_db)):
    return await Transactions.get_transactions(transid, request.headers['uid'], db)

@app.get('/transactions/verify/{transid}', tags = ['Transactions'])
async def verify_transactions(request: Request, transid: str, db: Session = Depends(get_db)):
    return await Transactions.verify(transid, db)

@app.post('/transactions/webhook', tags = ['Transactions'])
async def webhook_transaction(data: dict, request: Request, db: Session = Depends(get_db)):
    return await Transactions.webhook_transactions(data, db)

@app.post('/transactions/charge', tags = ['Transactions'])
async def charge_transaction(data: IChargeOrder, request: Request, db: Session = Depends(get_db)):
    return await Transactions.charge_transactions(data, db)

@app.post('/transactions/transfer', tags = ['Transactions'])
async def transfer_transaction(data: ITransfer, request: Request, db: Session = Depends(get_db)):
    return await Transactions.transfer_transactions(data, db)


# @app.delete('/transactions/cancel', tags = ['Transactions'])
# def webhook_transactions(data: dict, db: Session = Depends(get_db)):
#     return Transactions.get_transactions(data, db)


# @app.post('/pay/sources', tags = ['Payment Gateway Source'])
# def save_payment_source_authcode():
#     return Transactions.get_transactions()

# @app.get('/pay/sources', tags = ['Payment Gateway Source'])
# def get_payment_source_authcode():
#     return Transactions.get_transactions()
