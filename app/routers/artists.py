import urllib.parse
from ..internal.logger import logger
from ..db import models,artist_crud as db
from fastapi import APIRouter, HTTPException, Path, Query
from typing import List, Optional

LOG = logger(__name__)
router = APIRouter()

@router.get("/artists/", response_model=List[models.Artist])
def get_artists(genre: Optional[str] = Query(None, min_length=7, max_length=7, regex="^[a-zA-Z0-9]+$")):
    if genre is None:
        artists = db.get_all_artists()
    else:
        artists = db.get_artists_by_genre(genre)

    if artists is None:
        raise HTTPException(status_code=404, detail="No artists found.")
    else:
        return artists

@router.get("/artists/{artist_id}", response_model=models.Artist)
def get_artist(artist_id: str = Path(..., min_length=7, max_length=7, regex="^[a-zA-Z0-9]+$")):
    result = db.get_single_artist(artist_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    else:
        return result

@router.get("/artists/{artist_id}/albums", response_model=List[models.Album])
def get_artist_albums(artist_id: str = Path(..., min_length=7, max_length=7, regex="^[a-zA-Z0-9]+$")):
    artist_albums =  db.get_artist_albums(artist_id)
    if artist_albums is None:
        raise HTTPException(status_code=404, detail="No albums found.")
    else:
        return artist_albums
        