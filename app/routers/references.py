from typing import Optional
from fastapi import Depends, APIRouter

router = APIRouter()

""" Using dependencies + Optional """
def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

@router.get("/dependencies/")
def get_albums(commons: dict = Depends(common_parameters)):
    return commons

"""
    IDs for Testing
"""
# ARTIST#90c335b
# ALBUM#0f2a1cc
# GENRE#3844819