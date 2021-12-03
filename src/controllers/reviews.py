# from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from src.models.libs.mailing import EmailLib
from src.models.dbmodel.listings_model import *
from fastapi.responses import JSONResponse
from datetime import datetime
import ast
from fastapi.routing import APIRoute



class Reviews(APIRoute):

    def add_reviews(review_data: IReviews, db: Session):
        try:
            pass
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )

    def update_reviews(id: str, review_data: IReviews, db: Session):
        try:
            pass
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )