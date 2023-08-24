import base64
import boto3

from common.ContextAware import ContextAware
from media.S3MediaManager import S3MediaManager

base_url = 'http://aipif-2023.s3-website-us-west-1.amazonaws.com/_queue/'

class RqMediaManager(ContextAware):

    def __init__(self, mgr: S3MediaManager = S3MediaManager(), rq_prefix: str = '_queue/'):
        self._mgr = mgr
        self._rq_prefix = rq_prefix

    def file_read(self,rq_id: str, rq_suffix:str) -> bytes:
        s3_path = self.rq_id_to_s3_path(rq_id)
        return self._mgr.file_read(s3_path)

    def write(self, rq_id: str, rq_suffix:str, data: bytes):
        s3_path = self.rq_id_to_s3_path(rq_id)
        return self._mgr.file_write(s3_path, data)

    def rq_id_to_s3_path(self, rq_id: str, rq_suffix:str) -> str:
        return self.rq_prefix + rq_id + '_' + rq_suffix

