import boto3
import base64
from io import BytesIO
from uuid import uuid4
import os
from dotenv import load_dotenv
load_dotenv()
session = boto3.Session(
    aws_access_key_id= os.getenv('aws_access_key_id'),
    aws_secret_access_key= os.getenv('aws_secret_access_key'),
    region_name= os.getenv('region_name')
)
s3 = session.resource('s3')
def upload_file(blob_data, name):
    try:
        if len(blob_data) < 40:
            return ''
        file_data = base64.b64decode(blob_data)
        
        file_stream = BytesIO(file_data)
        print(file_stream)
        
        s3.Bucket('cosmos-bucket1').put_object(Key=f'{name}.png', Body=file_stream, ACL='public-read')
        return f'{os.getenv("aws_picture_url")}{name}.png'
    except Exception as e:
        print(e)
        return False