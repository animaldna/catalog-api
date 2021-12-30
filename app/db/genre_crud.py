import boto3
from . import models
from app.db.utilities import strip_ids
from boto3.dynamodb.conditions import Key
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')

def get_all_genres():
    response = catalog.query(
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
    