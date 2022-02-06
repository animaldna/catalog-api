import asyncio

from typing import List
from fastapi import APIRouter, HTTPException
from app.db import genre_crud as db
from app.db import models
from app.internal.logger import logger

LOG = logger(__name__)
router = APIRouter()

@router.get("/genres/")
async def get_genres():
    r = await db.get_all_genres()
    result = {"genres": r}
    if result is None:
        raise HTTPException(
            status_code=500, detail="Something went wrong." " Please try again later."
        )
    else:
        return result
