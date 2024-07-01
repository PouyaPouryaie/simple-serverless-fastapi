import boto3
from botocore.exceptions import ClientError
import logging
from uuid import uuid4
from .user_model import UserModel
from ...simple_exception import CustomException

class userSerivce():

    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        self.dynamo_table = self.dynamodb.Table('fast_api-sample')
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__) 

    def getUserById(self, userId: str):
        try:
            self.logger.info(f"User Id: {userId}")
            response = self.dynamo_table.get_item(Key={'user_id': userId})
            return response.get('Item')
        except ClientError as e:
            self.logger.info("Error: ", e)
            raise CustomException(404, f"Error: {e.response['Error']['Message']}")
        
    def addUser(self, user: UserModel):
        
        user.user_id = uuid4().hex

        try:
            self.dynamo_table.put_item(Item=user.to_dict())
            return user.to_dict()
        except ClientError as e:
            self.logger.info("Error: ", e)
            raise CustomException(400, e.response["Error"]["Message"])
