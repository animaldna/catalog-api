from . import models

def strip_ids(item, model):
    """Returns a model with human-friendly IDs by dropping '{item}#' prefix
    from the pk and/or sk."""
    options = {
        'artist': models.Artist,
        'album': models.Album,
        'genre': models.Genre
    }
    if model == 'album':
        return options[model](
            **item, id=item['sk'].partition('#')[2],
            artist_id=item['pk'].partition('#')[2])
    else:
        return options[model](**item, id=item['pk'].partition('#')[2])