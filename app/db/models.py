from typing import List, Dict
from pydantic import BaseModel

class AlbumBase(BaseModel):
    album_name: str
    price: float
    artist_name: str
    genre_id: str
    genre: str
    album_style: str
    release_year: int
    tracklist: List[Dict]
    album_imgs: Dict
    inventory: int = 0
    trending: bool
class AlbumInDB(AlbumBase):
    pk: str
    sk: str
class Album(AlbumBase):
    artist_id: str
    id: str
    

class ArtistBase(BaseModel):
    artist_name: str
    bio: str
    artist_imgs: Dict
    genre: str
    genre_id: str

class ArtistInDb(ArtistBase):
    pk: str
    sk: str

class Artist(ArtistBase):
    id: str   


class GenreBase(BaseModel):
    genre_name: str

class GenreInDb(GenreBase):
    pk: str
    item_type: str
class Genre(GenreBase):
    id: str

