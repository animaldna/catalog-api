import boto3
from . import models
from app.db.utilities import strip_ids
from boto3.dynamodb.conditions import Key
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')


def get_single_album(album_id: str):
    album_key = f'album#{album_id}'
    
    response = catalog.query(
        IndexName='type_sk_gsi',
        KeyConditionExpression=Key('item_type').eq('Album') &
        Key('sk').eq(album_key),
        ProjectionExpression="pk,sk,album_name,price, \
            artist_name,genre_id,genre,album_style,release_year, \
            tracklist,album_imgs,inventory,trending")

    try:
        album = response['Items'][0]
    except IndexError:
        result = None
    else: 
        result = models.Album(**album, 
            id=album['sk'].partition('#')[2],
            artist_id=album['pk'].partition('#')[2])
    
    return result
