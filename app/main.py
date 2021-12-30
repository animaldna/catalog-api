from fastapi import FastAPI
from app.routers import albums, artists, genres

app = FastAPI()

app.include_router(albums.router)
app.include_router(artists.router)
app.include_router(genres.router)

@app.get("/")
def root():
    return {
        "hello": "Welcome to the Conehead Records API",
        "api_version": "v1",
        "documentation_url": "thisapi.com/redoc"
    }
    