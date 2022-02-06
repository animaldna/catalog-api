import asyncio

from fastapi import APIRouter, HTTPException, Path, Query
from typing import Optional
from app.internal.logger import logger
from app.db import models, album_crud as db

LOG = logger(__name__)
router = APIRouter()

@router.get("/albums/{album_id}", response_model=models.Album)
async def get_album(
    album_id: str = Path(None, min_length=7, max_length=7, regex="^[a-zA-Z0-9]+$")):
    result = await db.get_single_album(album_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Album not found")
    else:
        return result
        