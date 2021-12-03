# from models.modules.core import logger, request, InvalidUsage, make_response, app, url_for
from src.models.libs.mailing import EmailLib
from src.models.dbmodel.listings_model import *
from src.models.dbmodel.accounts_model import AccountsModel
from fastapi.responses import JSONResponse
from datetime import datetime
import ast
from fastapi.routing import APIRoute
from uuid import uuid4


class CategoryListings(APIRoute):
    async def save_categorys(category_data: ICategory, db: Session):
        try:
            categoryinfo = db.query(CategoriesModel).filter(and_(
                CategoriesModel.name == category_data.name, CategoriesModel.parent == category_data.parent 
            )).first()

            if categoryinfo != None:
                return JSONResponse(status_code = 404, content = {
                    "error": "category found"
                })

            catinfo = CategoriesModel(
                name = category_data.name,
                parent = category_data.parent,
                summary = category_data.summary,
                subcategory = category_data.subcategory,
                image = category_data.image
            )
            db.add(catinfo)
            db.commit()
            db.close()

            return {
                "message": "category info saved"
            }
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )


    async def get_category(db: Session):
        try:
            category_data = db.query(CategoriesModel).all()
            db.close()

            return category_data
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )



class AdsListings(APIRoute):


    async def save_an_ads(ads_data: IAdsModel, _uid: str, db: Session):
        try:
            ads_data.ads_id = ads_data.ads_id if ads_data.ads_id != None else f"ads-{str(uuid4())}".replace("-", "")
            ads_data.uid = _uid

            adsinfo = db.query(AdsModel).filter(and_(
                AdsModel.name == ads_data.name, AdsModel.category == ads_data.category, AdsModel.uid == ads_data.uid, 
            )).first()

            if adsinfo != None:
                return JSONResponse(status_code = 404, content = {
                    "error": "ads info found"
                })

            ads_info = AdsModel(
                ads_id = ads_data.ads_id,
                uid = ads_data.uid,
                name = ads_data.name,
                price = ads_data.price,
                description = ads_data.description,
                images = str(ads_data.images),
                category = ads_data.category,
                brands = ads_data.brands,
                tags = str(ads_data.tags),
                isFeatured = ads_data.isFeatured,
                featuredName = ads_data.featuredName,
                is_commentable = ads_data.is_commentable,
                date_added = datetime.now(),
                date_updated = datetime.now()
            )

            db.add(ads_info)
            db.commit()
            db.refresh(ads_info)

            review_info = ReviewModel(
                ads_id = ads_data.ads_id,
                comments = str([]),
                likes = str([]),
                saved = str([]),
                dislike = str([])
            )
            db.add(review_info)
            db.commit()
            db.refresh(review_info)

            db.close()

            return {
                "message": "ads info saved",
                "ads_id": ads_data.ads_id
            }
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )


    async def search_ads(data: dict, db: Session, filter: bool = False, category: str = None, tags: str = None, brands: str = None):
        try:
            ads_data = []
            if filter == False:
                ads_data = db.query(AdsModel, ReviewModel).filter(or_(
                    AdsModel.name.like(data['search']), AdsModel.description.contains(data['search']), 
                    AdsModel.brands.like(data['search']), AdsModel.category.like(data['search']), AdsModel.tags.contains(data['search'])
                )).join(
                    ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                ).order_by(AdsModel.id.desc()).all() 
            else:
                ads_data = db.query(AdsModel, ReviewModel).filter(and_(
                    AdsModel.brands.like(brands), AdsModel.category.like(category), AdsModel.tags.contains(tags)
                )).join(
                    ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                ).order_by(AdsModel.id.desc()).all()

            db.close()

            if len(ads_data) == 0:
                return {
                    "message": []
                }

            results = []
            for ad in ads_data:
                ad_data = ad['AdsModel']
                ad_data.reviews = ad['ReviewModel']

                ad_data.images = ast.literal_eval(ad_data.images)
                ad_data.tags = ast.literal_eval(ad_data.tags)

                ad_data.reviews.saved = ast.literal_eval(ad_data.reviews.saved)
                ad_data.reviews.likes = ast.literal_eval(ad_data.reviews.likes)
                ad_data.reviews.comments = ast.literal_eval(ad_data.reviews.comments)
                ad_data.reviews.dislike = ast.literal_eval(ad_data.reviews.dislike)
                del ad_data.reviews.ads_id
                del ad_data.reviews.id

                results.append(ad_data)

            return {
                "message": results
            }
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )


    async def get_ads(ads_id: str, _uid: str, db: Session, limit: int = 100, isFeatured: bool = False, category: str = None, tags: str = None, brands: str = None):
        try:
            ads_data = []
            if ads_id == None and _uid == None:
                if isFeatured == False and tags == None and brands == None and category == None:
                    ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).join(
                        AccountsModel, AccountsModel.uid == AdsModel.uid
                    ).join(
                        CategoriesModel, CategoriesModel.name == AdsModel.category
                    ).join(
                        ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                    ).order_by(AdsModel.id.desc()).limit(limit).all()

                if isFeatured == True:
                    ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter_by(isFeatured = isFeatured).join(
                        AccountsModel, AccountsModel.uid == AdsModel.uid
                    ).join(
                        ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                    ).join(
                        CategoriesModel, CategoriesModel.name == AdsModel.category
                    ).order_by(AdsModel.id.desc()).limit(limit).all()

                if category != None:
                    ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter(or_(
                        AdsModel.category.like(category)
                    )).join(
                        AccountsModel, AccountsModel.uid == AdsModel.uid
                    ).join(
                        CategoriesModel, CategoriesModel.name == AdsModel.category
                    ).join(
                        ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                    ).order_by(AdsModel.id.desc()).limit(limit).all()

                if brands != None:
                    ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter(or_(
                        AdsModel.brands.like(brands)
                    )).join(
                        AccountsModel, AccountsModel.uid == AdsModel.uid
                    ).join(
                        CategoriesModel, CategoriesModel.name == AdsModel.category
                    ).join(
                        ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                    ).order_by(AdsModel.id.desc()).limit(limit).all()

                if tags != None:
                    ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter(or_(
                        AdsModel.tags.contains(tags)
                    )).join(
                        AccountsModel, AccountsModel.uid == AdsModel.uid
                    ).join(
                        CategoriesModel, CategoriesModel.name == AdsModel.category
                    ).join(
                        ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                    ).order_by(AdsModel.id.desc()).limit(limit).all()

            if _uid != None:
                ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter_by(uid = _uid).join(
                    CategoriesModel, CategoriesModel.name == AdsModel.category
                ).join(
                    AccountsModel, AccountsModel.uid == AdsModel.uid
                ).join(
                    ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                ).order_by(AdsModel.id.desc()).limit(limit).all()

            if ads_id != None:
                ads_data = db.query(AdsModel, AccountsModel, CategoriesModel, ReviewModel).filter_by(ads_id = ads_id).join(
                    CategoriesModel, CategoriesModel.name == AdsModel.category
                ).join(
                    AccountsModel, AccountsModel.uid == AdsModel.uid
                ).join(
                    ReviewModel, ReviewModel.ads_id == AdsModel.ads_id
                ).order_by(AdsModel.id.desc()).limit(limit).all()

            db.close()

            results = []
            for ad in ads_data:
                ad_data = ad['AdsModel']
                ad_data.reviews = ad['ReviewModel']
                ad_data.user = ad['AccountsModel']
                ad_data.category = ad['CategoriesModel']

                ad_data.images = ast.literal_eval(ad_data.images)
                ad_data.tags = ast.literal_eval(ad_data.tags)

                ad_data.reviews.saved = ast.literal_eval(ad_data.reviews.saved)
                ad_data.reviews.likes = ast.literal_eval(ad_data.reviews.likes)
                ad_data.reviews.comments = ast.literal_eval(ad_data.reviews.comments)
                ad_data.reviews.dislike = ast.literal_eval(ad_data.reviews.dislike)

                del ad_data.reviews.ads_id
                del ad_data.reviews.id
                del ad_data.user.id
                del ad_data.user.access
                del ad_data.category.id

                results.append(ad_data)

            return {
                "message": results
            }
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )


    async def update_ads(ads_data: IAdsModel, ads_id: str, db: Session):
        try:
            ads_info = db.query(AdsModel).filter_by(ads_id = ads_id).first()

            if ads_info == None:
                return JSONResponse(status_code = 404, content = {
                    "error": "ads info not found"
                })

            ads_info.name = ads_data.name
            ads_info.description = ads_data.description if ads_data.images != None else ads_info.description
            ads_info.price = ads_data.price if ads_data.price != None else ads_info.price
            ads_info.images = str(ads_data.images) if ads_data.images != None else ads_info.images
            ads_info.tags = str(ads_data.tags) if ads_data.tags != None else ads_info.tags
            ads_info.category = ads_data.category if ads_data.category != None else ads_info.category
            ads_info.brands = ads_data.brands if ads_data.brands != None else ads_info.brands
            ads_info.isFeatured = ads_data.isFeatured if ads_data.isFeatured != None else ads_info.isFeatured
            ads_info.featuredName = ads_data.featuredName if ads_data.featuredName != None else ads_info.featuredName

            db.add(ads_info)
            db.commit()
            db.close()
            return {
                "message": "ads info updated"
            }
        except Exception as e:
            return JSONResponse(status_code = 500, content = { "error":  str(e) } )


    async def delete_ads(ads_id: str, db: Session):
        try:
            ads_info = db.query(AdsModel).filter_by(ads_id = ads_id).first()

            if ads_info == None:
                return JSONResponse(status_code = 404, content = {
                    "error": "ads info not found"
                })

            review_info = db.query(ReviewModel).filter_by(ads_id = ads_id).first()

            db.delete(ads_info)
            db.delete(review_info)
            db.commit()
            db.close()

            return {
                "message": "ads info deleted"
            }
        except Exception as ex:
            raise Exception(str(ex))