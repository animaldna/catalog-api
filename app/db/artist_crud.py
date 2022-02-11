import boto3
from . import models
from ..internal.logger import logger
from ..db.utilities import strip_ids
from fastapi import HTTPException
from typing import Optional
from boto3.dynamodb.conditions import Key, Attr
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
LOG = logger(__name__)

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')

def get_single_artist(artist_id: str):
    """Query the main table with artist ID (as pk and sk)."""
    artist_key = f'artist#{artist_id}'
    response = catalog.get_item(Key={'pk': artist_key, 'sk': artist_key})

    try: 
        response = catalog.get_item(Key={'pk': artist_key, 'sk': artist_key})
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            artist = models.Artist(**response['Item'], 
                id=response['Item']['pk'].partition('#')[2])
        except KeyError:
            LOG.info('No results found')
            artist = None     
        
        return artist


def get_all_artists():
    """Query the type_name_gsi GSI for all item_type=Artist.""" 
    try:
        response = catalog.query(
            IndexName='type_name_gsi',
            KeyConditionExpression=Key('item_type').eq('Artist')
        )
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        if response['Count'] > 0:
            result = [strip_ids(item, 'artist') for item in response['Items']]
        else:
            # TODO -- Why would this happen? Need a better error.
            LOG.error('Something went wrong.')
            result = None
        
        return result  
    

def get_artists_by_genre(genre: str):
    try:
        response = catalog.query(
            IndexName='genre_name',
            KeyConditionExpression=Key('genre_id').eq(f'genre#{genre}') & 
            Key('item_name').begins_with('artist#')
        )
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        if response['Count'] > 0:
            result = [strip_ids(item, 'artist') for item in response['Items']]
        else:
            result = None    
        
        return result


def get_artist_albums(artist_id: str):
    artist_key = f'artist#{artist_id}'
    try: 
        response = catalog.query(
            KeyConditionExpression=(Key('pk').eq(artist_key) & 
                Key('sk').begins_with('album#'))
        )
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        if response['Items']:
            result = [strip_ids(item,'album') for item in response['Items']]   
        else: 
            result = None
        
        return result
    
