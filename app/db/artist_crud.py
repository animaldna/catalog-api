import boto3
from . import models
from typing import Optional
from app.db.utilities import strip_ids
from boto3.dynamodb.conditions import Key, Attr
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')

def get_single_artist(artist_id: str):
    """Query the main table with artist ID (as pk and sk)."""
    artist_key = f'artist#{artist_id}'
    response = catalog.get_item(Key={'pk': artist_key, 'sk': artist_key})

    try:
        artist = models.Artist(**response['Item'], 
            id=response['Item']['pk'].partition('#')[2])
    except KeyError:
        artist = None
    
    return artist      

def get_all_artists():
    """Query the type_name_gsi GSI for all item_type=Artist.""" 
    response = catalog.query(
        IndexName='type_name_gsi',
        KeyConditionExpression=Key('item_type').eq('Artist')
    )

    if response['Count'] > 0:
        result = [strip_ids(item, 'artist') for item in response['Items']]
    else:
        result = None
    
    return result  

def get_artists_by_genre(genre: str):
    response = catalog.query(
        IndexName='genre_name',
        KeyConditionExpression=Key('genre_id').eq(f'genre#{genre}') & 
        Key('item_name').begins_with('artist#')
    )
    if response['Count'] > 0:
        result = [strip_ids(item, 'artist') for item in response['Items']]
    else:
        result = None    
    
    return result

def get_artist_albums(artist_id: str):
    artist_key = f'artist#{artist_id}'
    response = catalog.query(
        KeyConditionExpression=(Key('pk').eq(artist_key) & 
            Key('sk').begins_with('album#'))
    )

    if response['Items']:
        print(response['Items'])
        result = [strip_ids(item,'album') for item in response['Items']]   
    else: 
        result = None
    
    return result
