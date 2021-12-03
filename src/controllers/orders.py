
from src.models.dbmodel.payment_model import *
from src.models.libs.paystack import Paystack_Gateway
from fastapi.responses import JSONResponse
import ast
from datetime import datetime
from uuid import uuid4


def choose_gateway(gateway: str = None):
    if(gateway == 'paystack'):
        _gateway = Paystack_Gateway()
    return _gateway


class Orders(object):

    async def get_orders(order_id: str, _uid: str, db: Session, limit: int = 100):
        try:
            orders = []
            transactions = []
            if _uid == None and order_id == None:
                orders = db.query(OrdersModel).all()
                transactions = db.query(TransactionsModel).all()
            else:
                orders = db.query(OrdersModel).filter_by(uid = _uid).all() if order_id == None else db.query(OrdersModel).filter_by(orderid = order_id).all()
                transactions = db.query(TransactionsModel).filter_by(uid = _uid).all() if order_id == None else db.query(TransactionsModel).filter_by(orderid = order_id).all()

            db.close()

            results = []
            for _order in orders:
                _order_transactions = await Orders.process_order_transactions(transactions, _order.orderid)
                print(_order.uid)
                orderinfo: dict = {
                    "orderid": _order.orderid,
                    "uid": _order.uid,
                    # "walletid": _order.walletid,
                    "summary": _order.summary,
                    "total_amount": int(_order.total_amount),
                    "amount_paid": _order_transactions['amount_paid'],
                    "payment_gateway": _order.payment_gateway,
                    "status": "completed" if _order_transactions['amount_paid'] == int(_order.total_amount) else _order.status,
                    "order_type": _order.order_type,
                    "date_updated": _order.date_updated,
                    "transactions": _order_transactions['transactions'][::-1],
                }

                results.append(orderinfo)

            return {
                "message": results
            }
        except Exception as e:
            print(str(e))
            # return JSONResponse(status_code = 500, error = str(e))

    async def update_order(orderid: str, order_info, db: Session):
        try:
            _orderinfo = db.query(OrdersModel).filter_by(orderid = orderid).first()
            if _orderinfo == None:
                return JSONResponse( status_code = 400, content = { "error": "order not found" })
                
            _orderinfo.status = order_info.status if order_info.status != None else _orderinfo.status
            _orderinfo.summary = order_info.summary if order_info.summary != None else _orderinfo.summary
            _orderinfo.total_amount = str(order_info.total_amount)
            _orderinfo.payment_gateway = order_info.payment_gateway if "payment_gateway" in order_info else _orderinfo.payment_gateway
            _orderinfo.order_type = order_info.order_type
            
            db.add(_orderinfo)
            db.commit()
            db.close()
            

            return {
                "message": "order updated"
            }
        except exc.SQLAlchemyError as e:
            return JSONResponse( status_code = 500, content = { "error":  str(e) })
        except Exception as e:
            return JSONResponse( status_code = 500, content = { "error": str(e) })

    async def save_order(order_info, _uid: str, db: Session):
        try:
            order_id = order_info.orderid if order_info.orderid != None else str(uuid4())
            _orderinfo = db.query(OrdersModel).filter_by(orderid = order_id).first()
            if _orderinfo != None:
                return JSONResponse( status_code = 400, content = { "error": "order found" })
                

            orders_info = OrdersModel(
                orderid = order_id,
                uid = _uid,
                summary = order_info.summary if order_info.summary != None else '',
                total_amount = order_info.total_amount if order_info.total_amount != None else 0,
                order_type = order_info.order_type,
                status = order_info.status if order_info.status != None else False,
                payment_gateway = order_info.payment_gateway if order_info.payment_gateway != None else 'cash',
                date_added = datetime.now(),
                date_updated = datetime.now()
            )
            db.add(orders_info)
            db.commit()
            db.close()
            
            return {
                "message": "order saved",
                "orderid": order_id
            }
        except Exception as e:
            return JSONResponse(status_code = 500, error = str(e))

    async def process_order_transactions(transactions: any, orderid: any):
        try:
            _processed: dict = {
                'transactions': [],
                'amount_paid': 0.00
            }
            if transactions != None:
                for _trans in transactions:
                    if _trans.orderid == orderid:
                        if _trans.status == 'successful' or _trans.status == 'success':
                            _processed['amount_paid'] = float(_processed['amount_paid']) + float(_trans.amount)
                        _trans.transaction_info = ast.literal_eval(_trans.transaction_info)
                        _processed['transactions'].append(_trans)
            return _processed
        except Exception as e:
            raise Exception(str(e))


    def validate_order(orderid, db: Session):
        order_info = db.query(OrdersModel).filter_by(orderid = orderid).first()
        if order_info == None:
            raise Exception("order not found")
        return order_info



class Transactions(object):
    

    ####  transactions functions
    async def get_transactions(transid: str, _uid: str, db: Session, limit: int = 100):
        try:
            if _uid == None:
                transactions = db.query(TransactionsModel).limit(limit).all()
            elif _uid != None:
                transactions = db.query(TransactionsModel).filter_by(uid = _uid).limit(limit).all() if transid == None else db.query(TransactionsModel).filter_by(transid = transid).limit(limit).all()
            db.close()
            

            results = []
            for transaction in transactions:
                transaction.transaction_info = ast.literal_eval(transaction.transaction_info)
                results.append(transaction)

            return {
                "message": results
            }
        except Exception as e:
            print(str(e))
            # return JSONResponse(status_code = 500, error = str(e))

    async def save_transactions(transaction_info: ITransactions, _uid: str, db: Session):
        try:
            orderinfo = Orders.validate_order(transaction_info.orderid, db)
            
            transaction_info.transid = transaction_info.transid if transaction_info.transid != None else f"ref-{str(uuid4())}"

            _transinfo = db.query(TransactionsModel).filter_by(transid = transaction_info.transid).first()
            if _transinfo != None:
                return JSONResponse( status_code = 400, content = { "error": "transaction found" })

            transaction_info.transaction_info: any = ast.literal_eval(transaction_info.transaction_info)

            if 'source' in transaction_info.transaction_info and transaction_info.transaction_info['source'] != 'cash':
                _verified_transinfo = await Transactions.verify_payment_gateway_transaction(transaction_info.transid, transaction_info.transaction_info['source'])
                transaction_info.status = _verified_transinfo['status']
                transaction_info.amount = _verified_transinfo['amount'] if transaction_info.transaction_info['source'] != 'paystack' else _verified_transinfo['amount'] / 100

                if transaction_info.transaction_info['source'] == 'paystack':
                    transaction_info.transaction_info['channel'] = _verified_transinfo['channel']
                    transaction_info.transaction_info['customer'] = _verified_transinfo['customer']
                    transaction_info.transaction_info['authorization'] = _verified_transinfo['authorization']

            trans_info = TransactionsModel(
                orderid = transaction_info.orderid,
                transid = transaction_info.transid if transaction_info.transid != None else f"ref-{str(uuid4())}",
                uid = _uid,
                summary = transaction_info.summary if transaction_info.summary != None else '',
                amount = transaction_info.amount if transaction_info.amount != None else 0,
                status = transaction_info.status if transaction_info.status != None else 'not set',
                type = transaction_info.type if transaction_info.type != None else 'not set',
                transaction_info = str(transaction_info.transaction_info) if transaction_info.transaction_info != None else str([]),
                date_added = datetime.now(),
                date_updated = datetime.now()
            )
            db.add(trans_info)
            db.commit()
            db.close()
            
            return {
                "message": "transaction saved"
            }
        except Exception as e:
            return JSONResponse( status_code = 500, content = { "error": str(e) })

    async def verify(transid: str, db: Session):
        try:
            _transinfo = db.query(TransactionsModel).filter_by(transid = transid).first()
            if _transinfo == None:
                return JSONResponse( status_code = 404, content = { "error": "transaction not found" })

            orderinfo = Orders.validate_order(_transinfo.orderid, db)

            _transinfo.transaction_info = ast.literal_eval(_transinfo.transaction_info)
            print(_transinfo.transaction_info['source'])

            if 'source' in _transinfo.transaction_info and _transinfo.transaction_info['source'] != 'cash':
                _verified_transinfo = await Transactions.verify_payment_gateway_transaction(transid, _transinfo.transaction_info['source'])
                _transinfo.status = _verified_transinfo['status']
                _transinfo.amount = _verified_transinfo['amount'] if _transinfo.transaction_info['source'] != 'paystack' else _verified_transinfo['amount'] / 100

            # transinfo = _transinfo
            # transinfo['orderinfo'] = orderinfo

            return {
                "message": _transinfo
            }
        except Exception as e:
            print(str(e))
            return JSONResponse( status_code = 404, content = { "error": str(e) })

    async def verify_payment_gateway_transaction(transid: str, source: str = 'paystack'):
        try:
            gateway = choose_gateway(source)
            _verify_resp = gateway.verify_transaction(transid)
            if _verify_resp['status'] == False:
                raise Exception(_verify_resp['message'])

            return _verify_resp['data']
        except Exception as e:
            raise Exception(str(e))

    async def webhook_transactions(data: any, db: Session):
        try:
            transInfo = await Transactions.verify(data['data']['reference'], db)
            return transInfo
        except Exception as e:
            return JSONResponse( status_code = 404, content = { "error": str(e) })

    async def charge_transactions(data: IChargeOrder, db: Session):
        try:
            resp = {}
            Orders.table = Transactions.table
            Orders.validate_order(data.orderid, db)
            data.transid = f"ref-{str(uuid4())}"

            # charge payment gateway for transaction
            if data.payment_source != 'cash':
                gateway = choose_gateway(data.payment_source)
                resp = await gateway.charge_user(data, data.charge_type)
                if resp['status'] == False:
                    raise Exception(resp['message'])
                    # resp['source'] = data.payment_source
                    # resp['status'] = 'failed'
                    # data.summary = resp['message'] if 'message' in resp else resp['error']

            # confirm order then verify and save transaction info
            _trans = ITransactions(
                orderid = data.orderid,
                transid = data.transid,
                uid = data.uid,
                type = "not set",
                summary = data.summary,
                amount = data.amount,
                status = "successful" if 'status' in resp and resp['status'] == True else 'failed' if data.payment_source != 'cash' else 'successful',
                transaction_info = str(resp['data']) if resp != {} else str({
                    "source": data.payment_source
                })
            )
            saved_trans = await Transactions.save_transactions(_trans, data.uid, db)
            if "body" in saved_trans:
                raise Exception(saved_trans['body'])
            return {
                "message": {
                    "msg": "charged successfully",
                    "ref": data.transid
                }
            }
        except Exception as e:
            return JSONResponse( status_code = 500, content = { "error": str(e) })
    
    async def transfer_transactions(data: ITransfer, db: Session):
        try:
            # charge payment gateway for transaction
            gateway = choose_gateway(data.payment_source)
            resp = gateway.transfer_transaction(data)
            
            Orders.table = Transactions.table
            # save order info
            orderinfo = await Orders.save_order({
                "summary": data.summary if data.summary != None else '',
                "total_amount": data.amount,
                "order_type": "one time",
                "status": resp.status,
                "payment_gateway": data.payment_source
            }, data.uid, db)

            # confirm order then verify and save transaction info
            saved_trans = await Transactions.save_transactions({
                "orderid": orderinfo.orderid,
                "transid": resp.transid,
                "uid": data.uid,
                "summary": data.summary,
                "amount": resp.amount,
                "status": resp.status,
                "transaction_info": resp
            }, orderinfo.uid, db)
            return {
                "message": "transfer complete"
            }
        except Exception as e:
            return JSONResponse( status_code = 404, content = { "error": str(e) })

    