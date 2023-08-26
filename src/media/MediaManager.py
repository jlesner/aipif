import base64

# TODO remove and route calls to src/media/B64MediaManager.py

from common.ContextAware import ContextAware

class MediaManager(ContextAware):

    def bytes_to_url(self, data:bytes, mime_type: str) -> str:
        return f'data:{mime_type};base64,' \
            + base64.b64encode(data).decode('utf-8')
    
    def bytes_to_png_url(self, data:bytes) -> str:
        return self.bytes_to_url(data, 'image/png')
    
    def bytes_to_jpg_url(self, data:bytes) -> str:
        return self.bytes_to_url(data, 'image/jpg')

    def bytes_to_mp4_url(self, data:bytes) -> str:
        return self.bytes_to_url(data, 'audio/mp4')
    
    def bytes_to_wav_url(self, data:bytes):
        return self.bytes_to_url(data, 'audio/wav')

    def url_to_bytes(self, data_url: str) -> bytes:
        if not data_url.startswith('data:'):
            raise ValueError("Invalid data URL format")
        base64_data = data_url.split(',', 1)[1]
        return base64.b64decode(base64_data)
