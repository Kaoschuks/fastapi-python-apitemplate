# from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from src.models.libs.mailing import EmailLib
from src.models.dbmodel.listings_model import *
from fastapi.responses import JSONResponse
from datetime import datetime
import ast



class Reviews(object):

    def add_reviews():
        try:
            pass
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )

    def update_reviews(id):
        try:
            pass
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )