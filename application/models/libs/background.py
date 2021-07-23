from apscheduler.schedulers.asyncio import AsyncIOScheduler
from application.models.core import app
import pytz

hour = 0

# @app.on_event('startup')
# async def schedule_event():
#     scheduler = AsyncIOScheduler(timezone=pytz.utc)
#     scheduler.start()
#     scheduler.add_job(func_name, "cron", hour=hour)  # runs every night at midnight


# def func_name():
#     print(app)