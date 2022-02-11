from ..db import genre_crud as db
from ..db import models
from ..internal.logger import logger
from typing import List
from fastapi import APIRouter, HTTPException


LOG = logger(__name__)
router = APIRouter()

@router.get("/genres/")
def get_genres():
    result = {"genres": db.get_all_genres()}
    if result is None:
        # TODO - This shouldn't happen. Need more info.
        raise HTTPException(
            status_code=500, detail="Something went wrong." " Please try again later."
        )
    else:
        return result
