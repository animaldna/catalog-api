from fastapi import FastAPI
from app.routers import albums, artists, genres

from starlette.applications import Starlette
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded


limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(genres.router)

@app.get("/")
@limiter.exempt
def root():
    return {
        "hello": "Welcome to the Conehead Records API",
        "api_version": "lol not sure",
        "documentation_url": "https://catalog-api.chloeboylan.work/redoc"
    }
    