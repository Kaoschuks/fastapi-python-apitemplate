from src.models.libs.proxylib import ProxyLib
from paystackapi.paystack import Paystack
from src.models.core import app, os

class Paystack_Gateway(object):
    paystack = {}
    request = {
        "url": "",
        "method": "GET",
        "headers": {
            "accept": "application/json",
            "Authorization": "Bearer ",
        }
    }

    def __init__(self):
        self.paystack = Paystack(secret_key = "sk_test_b54458f05ba3a70e362f775e5b7b0b1b256966b8")
        self.request['headers']['Authorization'] = "Bearer sk_test_b54458f05ba3a70e362f775e5b7b0b1b256966b8"

    ####  transactions functions
            
    def get_transactions(self, transid: str):
        try:
            return self.paystack.transaction.list() if transid == None else self.paystack.transaction.list(transid)
        except Exception as e:
            raise Exception(str(e))

    def init_transaction(self, payload):
        try:
            return self.paystack.transaction.initialize(
                reference = payload.transid,
                amount = payload.amount * 100, 
                email = payload.email
            )
        except Exception as e:
            raise Exception(str(e))

    def verify_transaction(self, ref: str):
        try:
            return self.paystack.transaction.verify(ref)
        except Exception as e:
            raise Exception(str(e))

    async def __create_transfer_recipient(self, userinfo = {}):
        try:
            return await ProxyLib.make_request(self.request, { 
                "type": "nuban", 
                "name": userinfo.name, 
                "account_number": userinfo.account_number, 
                "bank_code": userinfo.bankcode, 
                "currency": userinfo.currency
            })
        except Exception as e:
            raise Exception(str(e))

    async def init_transfer_transaction(self, transinfo = {}):
        try:
            recipient = await self.__create_transfer_recipient(transinfo.recipient)
            if  recipient.status == False:
                raise Exception(recipient.message)

            return self.paystack.transfer.initiate(
                source = 'balance',
                reason = transinfo.summary,
                amount = transinfo.amount * 100,
                recipient = recipient.data.recipient_code,
            )
        except Exception as e:
            raise Exception(str(e))

    def cancel_transaction(self, transinfo = {}):
        try:
            pass
        except Exception as e:
            raise Exception(str(e))

    def confirm_transaction_status_webhook(self, customerinfo = {}):
        try:
            pass
        except Exception as e:
            raise Exception(str(e))

    async def charge_user(self, payload, type = "token", country = "ng"):
        try:
            if type == 'card':
                return self.paystack.transaction.charge(
                    reference = payload.transid,
                    authorization_code = payload.authcode,
                    email = payload.email,
                    amount = payload.amount * 100
                )
            # if type == 'token':
            #     return self.paystack.transaction.charge_token(
            #         reference='reference',
            #         token='token', email='email',
            #         amount='amount'
            #     )
        except Exception as e:
            raise Exception(str(e))