from fastapi.responses import HTMLResponse
from src.core import engine, Base, redis, app, os, uvicorn
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

@app.on_event("startup")
async def startup_event():
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown_events():
    await redis.close()
    await engine.dispose()

@app.get("/", response_class=HTMLResponse)
def index():
    return """
<!Doctype html>
    <html>
        <body>
            <h1>SecureAPI</h1>
            <div class="btn-group">
                <a href="/docs"><button>SwaggerUI</button></a>
                <a href="/redoc"><button>Redoc</button></a>
            </div>
        </body>
    </html>
"""


if __name__ == "__main__":
    uvicorn.run(
        app, 
        reload = True, 
        log_level="debug", 
        port=int(os.getenv("PORT"),
        loop="uvloop"
    ))