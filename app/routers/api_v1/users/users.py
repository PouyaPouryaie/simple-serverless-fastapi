from fastapi import APIRouter, HTTPException
import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal
from uuid import uuid4
from .user_model import UserModel
from .user_service import userSerivce

router = APIRouter()

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
dynamo_table = dynamodb.Table('fast_api-sample')
userSerivce = userSerivce()

@router.get("")
async def get_users():
    try:
        scan_params = {
            'TableName': dynamo_table.name
        }

        return build_response(200, scan_dynamo_records(scan_params, []))
    except ClientError as e:
        print('Error: ', e)
        return build_response(400, e.response['Error']['Message'])

@router.get("/{userId}")
async def get_user_by_id(userId: str):

    response = userSerivce.getUserById(userId)
    if response is not None:
        return build_response(200, response)
    raise HTTPException(status_code=404, detail=f"user not found, {userId}")

@router.post("")
async def add_user(user: UserModel):


    response = userSerivce.addUser(user)
    body = {
        'Operation': 'SAVE',
        'Message': 'SUCCESS',
        'Item': user.to_dict()
    }

    return build_response(200, body)


def scan_dynamo_records(scan_params, item_array):
    response = dynamo_table.scan(**scan_params)
    item_array.extend(response.get('Items', []))

    if 'LastEvaluatedKey' in response:
        scan_params['ExclusiveStartKey'] = response['LastEvaluatedKey']
        return scan_dynamo_records(scan_params, item_array)
    else:
        return {'users': item_array}
    

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-type':'application/json'
        },
        'body':use_encoder(body)
    }

def use_encoder(body):
    response = json.dumps(body, cls=DecimalEncoder)
    data = json.loads(response)
    return data

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # Check if it's an int or a float
            if obj % 1 == 0:
                return int(obj)
            else:
                return float(obj)
        # Let the base class default method raise the TypeError
        return super(DecimalEncoder, self).default(obj)