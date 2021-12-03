from src.models.core import custom_openapi, os, app
from src.models.configs.dbconfig  import Base, engine
from src.views.users_route import *
from src.views.notification_route import *
from src.views.ads_route import *
from src.views.orders_route import *
from src.views.transactions_route import *
from src.views.messaging_route import *

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

#  sample rest api implememtation
@app.get('/')
def index():
    return { 'documentation': "localhost:" + os.getenv("PORT") + "/docs"}

app.openapi = custom_openapi