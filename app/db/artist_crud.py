import asyncio
import aioboto3

from . import models
from typing import Optional
from app.db.utilities import strip_ids
from boto3.dynamodb.conditions import Key, Attr
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

async def get_single_artist(artist_id: str):
    """Query the main table with artist ID (as pk and sk)."""
    artist_key = f'artist#{artist_id}'
    session = aioboto3.Session()
    
    async with session.resource('dynamodb') as ddb:
        catalog = await ddb.Table('catalog_v2')
        response = await catalog.get_item(
            Key={'pk': artist_key, 'sk': artist_key}
        )
        try:
            artist = models.Artist(**response['Item'], 
                id=response['Item']['pk'].partition('#')[2])
        except KeyError:
            artist = None
        
        return artist      

async def get_all_artists():
    """Query the type_name_gsi GSI for all item_type=Artist.""" 
    session = aioboto3.Session()
    async with session.resource('dynamodb') as ddb:
        catalog = await ddb.Table('catalog_v2')
        response = await catalog.query(
            IndexName='type_name_gsi',
            KeyConditionExpression=Key('item_type').eq('Artist')
        )

        if response['Count'] > 0:
            result = [strip_ids(item, 'artist') for item in response['Items']]
        else:
            result = None
        
        return result  

async def get_artists_by_genre(genre: str):
    session = aioboto3.Session()
    async with session.resource('dynamodb') as ddb:
        catalog = await ddb.Table('catalog_v2')
        response = await catalog.query(
            IndexName='genre_name',
            KeyConditionExpression=Key('genre_id').eq(f'genre#{genre}') & 
            Key('item_name').begins_with('artist#')
        )
        if response['Count'] > 0:
            result = [strip_ids(item, 'artist') for item in response['Items']]
        else:
            result = None    
        
        return result

async def get_artist_albums(artist_id: str):
    session = aioboto3.Session()
    artist_key = f'artist#{artist_id}'
    async with session.resource('dynamodb') as ddb:
        catalog = await ddb.Table('catalog_v2')
        response = await catalog.query(
            KeyConditionExpression=(Key('pk').eq(artist_key) & 
                Key('sk').begins_with('album#'))
        )

        if response['Items']:
            result = [strip_ids(item,'album') for item in response['Items']]   
        else: 
            result = None
        
        return result
