import boto3
from . import models
from ..internal.logger import logger
from ..db.utilities import strip_ids
from fastapi import HTTPException
from boto3.dynamodb.conditions import Key
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')


def get_single_album(album_id: str):
    album_key = f'album#{album_id}'
    
    try: 
        response = catalog.query(
            IndexName='type_sk_gsi',
            KeyConditionExpression=Key('item_type').eq('Album') &
            Key('sk').eq(album_key),
            ProjectionExpression="pk,sk,album_name,price, \
                artist_name,genre_id,genre,album_style,release_year, \
                tracklist,album_imgs,inventory,trending"
        )
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            album = response['Items'][0]
        except IndexError:
            result = None
        else: 
            result = models.Album(**album, 
                id=album['sk'].partition('#')[2],
                artist_id=album['pk'].partition('#')[2])
        
        return result

