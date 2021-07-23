from application.views.route import *
from application.models.core import app, os

if __name__ == "__main__":
    uvicorn.run(
        app, 
        reload = True, 
        log_level="debug", 
        port=int(os.getenv("PORT"))
    )