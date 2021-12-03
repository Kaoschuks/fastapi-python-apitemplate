from src.controllers.ads import *
from src.models.core import app, Depends
from fastapi import APIRouter
from src.models.libs.jwt import AuthJWT, validate_token


ads_router = APIRouter(route_class = AdsListings)
category_router = APIRouter(route_class = CategoryListings)



@category_router.get("/all", operation_id="authorize")
async def get_ads_category(db: Session = Depends(get_db)):
    return await CategoryListings.get_category(db)

@category_router.post("", operation_id="authorize")
async def save_ads_category(category_data: ICategory, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await CategoryListings.save_categorys(category_data, db)

@category_router.put("/{category_id}", operation_id="authorize")
async def update_ads_category(category_id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await CategoryListings.get_category(db)





@ads_router.post("", operation_id="authorize")
async def save_ads_listings(data: IAdsModel, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await AdsListings.save_an_ads(data, uid, db)

@ads_router.post("/search")
async def search_for_ad(data: dict, db: Session = Depends(get_db)):
    return await AdsListings.search_ads(data, db)

@ads_router.post("/filter")
async def search_for_ad(db: Session = Depends(get_db), category: Optional[str] = None, tags: Optional[str] = None, brands: Optional[str] = None):
    return await AdsListings.search_ads({}, db, True, category, tags, brands)

@ads_router.get("", operation_id="authorize")
async def get_user_ads(limit: Optional[int] = 100, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    uid = validate_token(Authorize)
    return await AdsListings.get_ads(None, uid, db)

@ads_router.get("/all")
async def get_all_ads_listing(tags: Optional[str] = None, isFeatured: Optional[bool] = False, category: Optional[str] = None, brands: Optional[str] = None, limit: Optional[int] = 100, db: Session = Depends(get_db)):
    return await AdsListings.get_ads(None, None, db, limit, isFeatured, category, tags, brands)

@ads_router.get("/{ads_id}")
async def get_ads_by_id(ads_id: str = None, db: Session = Depends(get_db)):
    return await AdsListings.get_ads(ads_id, None, db)

@ads_router.put("/{ads_id}", operation_id="authorize")
async def update_ads_info(data: IAdsModel, ads_id: str = None, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    return await AdsListings.update_ads(data, ads_id, db)

@ads_router.delete("/{ads_id}", operation_id="authorize")
async def delete_ads_info(ads_id: str = None, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    validate_token(Authorize)
    return await AdsListings.delete_ads(ads_id, db)




app.include_router(ads_router, prefix="/listings", tags = ['Ads Listing Management'])
app.include_router(category_router, prefix="/listings/categories", tags = ['Ads Listing Management'])