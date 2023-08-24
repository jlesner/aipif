from common.ContextAware import ContextAware
from media.S3MediaManager import S3MediaManager

base_url = 'http://aipif-2023.s3.amazonaws.com/_asset/'

class RqMediaManager(ContextAware):

    def __init__(self, mgr: S3MediaManager = S3MediaManager(), rq_prefix: str = '_asset/'):
        self._mgr = mgr
        self._rq_prefix = rq_prefix

    def _s3_path_make(self, rq_id: str, rq_suffix:str) -> str:
        return self._rq_prefix + rq_id + rq_suffix

    def file_read(self,rq_id: str, rq_suffix:str) -> bytes:
        s3_path = self._s3_path_make(rq_id, rq_suffix)
        return self._mgr.file_read(s3_path)

    def file_write(self, rq_id: str, rq_suffix:str, data: bytes, content_type: str) -> str:
        s3_path = self._s3_path_make(rq_id, rq_suffix)
        return self._mgr.file_write(s3_path, data, content_type)

    def file_list(self):
        return self._mgr.file_list(self._rq_prefix)
