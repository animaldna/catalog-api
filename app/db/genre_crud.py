import boto3
from . import models
from ..internal.logger import logger
from ..db.utilities import strip_ids
from fastapi import HTTPException
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
LOG = logger(__name__)

ddb = boto3.resource('dynamodb')
catalog = ddb.Table('catalog_v2')

def get_all_genres():
    try: 
        response = catalog.query(
            IndexName='type_name_gsi', 
            KeyConditionExpression=Key('item_type').eq('Genre'),
            ProjectionExpression="pk, genre_name"
        )
    except ClientError as e:
        LOG.error(e, exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            result = response['Items']
        except KeyError:
            # TODO - This shouldn't happen. Need more info.
            LOG.info('No results found')
            result = None
        else:
            result = [strip_ids(item, 'genre') for item in response['Items']]
        
        return result
    
    