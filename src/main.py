from src.models.core import app, os
from src.views.route import *

# if __name__ == "__main__":
#     uvicorn.run(
#         app, 
#         reload = True, 
#         log_level="debug", 
#         port=int(os.getenv("PORT"))
#     )