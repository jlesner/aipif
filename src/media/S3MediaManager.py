import base64
import boto3

from common.ContextAware import ContextAware

# base_url = 'http://aipif-2023.s3.amazonaws.com/'

class S3MediaManager(ContextAware):

    def __init__(self, bucket_name: str = 'aipif-2023'):
        self._s3_client = boto3.client('s3')
        self._bucket_name = bucket_name

    def file_read(self, object_key: str) -> bytes:
        response = self._s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
        return response['Body'].read()

    def file_write(self, object_key: str, data: bytes, content_type: str) -> str:
        self._s3_client.put_object(Bucket=self._bucket_name, Key=object_key, Body=data, ContentType=content_type)
        return f'http://{self._bucket_name}.s3.amazonaws.com/{object_key}'

    def file_list(self, path=''):
        try:
            response = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix=path)
            if 'Contents' in response:
                contents = [obj['Key'] for obj in response['Contents']]
                return contents
            else:
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []