import pytest


@pytest.fixture()
def sample_artist():
    data = {
        "artist_name": "Nine Inch Nails",
        "bio": "Industrial rock band Nine Inch Nails was formed in 1988 by Trent Reznor in Cleveland, Ohio. Reznor has served as the main producer, singer, songwriter, instrumentalist, and sole member of Nine Inch Nails for 28 years.",
        "artist_imgs": {
            "primary": "/images/catalog/artists/90c335b/profile/originals/Nine Inch Nails_primary.jpg",
            "thumbnail_200": "/images/catalog/artists/90c335b/profile/thumbnails/Nine Inch Nails_primary_200.jpg",
        },
        "genre": "Electronic", 
        "genre_id": "genre#555eb91",
        "id": "90c335b"
    }
    return data


@pytest.fixture()
def sample_album():
    data = {
        "album_name": "Pinion",
        "price": 29.99,
        "artist_name": "Nine Inch Nails",
        "genre_id": "genre#1813588",
        "genre": "Electronic",
        "album_style": "Industrial",
        "release_year": 1995,
        "tracklist": [
            {
                "track": "Pinion",
                "duration": "1:24"
            }
        ],
        "album_imgs": {
            "primary": "/images/catalog/artists/90c335b/albums/12d3232/originals/Pinion_primary.jpg",
            "thumbnail_200": "/images/catalog/artists/90c335b/albums/12d3232/thumbnails/Pinion_primary_200.jpg",
        },
        "inventory": 81,
        "trending": True,
        "artist_id": "90c335b",
        "id": "12d3232"
    }
    return data


@pytest.fixture()
def sample_genres():
    data = [
        {
            "genre_name": "Electronic",
            "id": "1813588"
        },
        {
            "genre_name": "Folk, World, & Country",
            "id": "3844819"
        },
        {
            "genre_name": "Jazz",
            "id": "6230003"
        },
        {
            "genre_name": "Pop",
            "id": "30dk34hf"
        },
        {
            "genre_name": "Rock",
            "id": "cdf9e60"
        },
        {
            "genre_name": "Stage & Screen",
            "id": "2390396"
        }
    ]
    return data


@pytest.fixture()
def artist_validation_error():
    data = {
        "detail": [
            {
                "loc": [
                    "path",
                    "artist_id"
                ],
                "msg": "string does not match regex \"^[a-zA-Z0-9]+$\"",
                "type": "value_error.str.regex",
                "ctx": {
                    "pattern": "^[a-zA-Z0-9]+$"
                }
            }
        ]
    }
    return data


@pytest.fixture()
def album_validation_error():
    data = {
        "detail": [
            {
                "loc": [
                    "path",
                    "album_id"
                ],
                "msg": "string does not match regex \"^[a-zA-Z0-9]+$\"",
                "type": "value_error.str.regex",
                "ctx": {
                    "pattern": "^[a-zA-Z0-9]+$"
                }
            }
        ]
    }
    return data
