from application.models.dbmodel.demo_model import IRecord, ILogin, Record, Session, Depends, get_db
from application.models.libs.jwt import generatejwt, AuthJWT

class Demo(object):
    def getalldemodata(db: Session):
        users = db.query(Record).all()
        db.close()
        return users

    async def savedemodata(db: Session, data: IRecord):
        rec = Record(date = data.date, country = data.country, cases = data.cases, deaths = data.deaths, recoveries = data.recoveries)
        db.add(rec)
        db.commit()
        db.refresh(rec)
        return rec

    def savetoken(formdata: dict, Authorize: AuthJWT):
        if not formdata:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # print(formdata)
        formdata['uid'] = 6232
        access_token = generatejwt(formdata, Authorize)
        return access_token
