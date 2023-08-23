import base64
import boto3

from common.ContextAware import ContextAware

base_url = 'http://aipif-2023.s3-website-us-west-1.amazonaws.com/_queue/'

class S3MediaManager(ContextAware):

    def __init__(self, bucket_name: str = 'aipif-2023'):
        self._s3_client = boto3.client('s3')

    def s3_binary_file_read(self,bucket_name: str, object_key: str) -> bytes:
        """
        Fetches an S3 object's contents and returns it as bytes.
        
        Parameters:
        - bucket_name (str): Name of the S3 bucket.
        - object_key (str): Key (path) of the object inside the bucket.
        
        Returns:
        - bytes: Content of the S3 object.
        """
        response = self._s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read()


    def s3_binary_file_write(self, bucket_name: str, object_key: str, data: bytes):
        """
        Uploads byte data as an S3 object.
        
        Parameters:
        - bucket_name (str): Name of the S3 bucket.
        - object_key (str): Key (path) where the byte data should be stored in the bucket.
        - data (bytes): Data to be uploaded.
        """
        self._s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=data)


# # Example Usage
# bucket_name = 'aipif-2023'
# object_key = 'path/in/s3/filename.ext'

# mgr = S3MediaManager()
# content = mgr.s3_binary_file_read(bucket_name, object_key)
# mgr.s3_binary_file_write(bucket_name, object_key, content)

