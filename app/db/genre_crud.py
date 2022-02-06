# import boto3
import asyncio
import aioboto3 

from . import models
from app.db.utilities import strip_ids
from boto3.dynamodb.conditions import Key
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

async def get_all_genres():
    session = aioboto3.Session()
    async with session.resource('dynamodb') as ddb:
        catalog = await ddb.Table('catalog_v2')

        response = await catalog.query(
            IndexName='type_name_gsi', 
            KeyConditionExpression=Key('item_type').eq('Genre'),
            ProjectionExpression="pk, genre_name"
        )
        try:
            result = response['Items']
        except KeyError:
            result = None
        else:
            result = [strip_ids(item, 'genre') for item in response['Items']]
        
        return result

def add_genre(genre):
    pass
    