import base64

from common.ContextAware import ContextAware

class B64MediaManager(ContextAware):

    def bytes_to_png_url(data:bytes) -> str:
        return 'data:image/png;base64,' \
            + base64.b64encode(data).decode('utf-8')
    
    def bytes_to_jpg_url(data:bytes) -> str:
        return 'data:image/jpg;base64,' \
            + base64.b64encode(data).decode('utf-8')

    def url_to_bytes(data_url: str) -> bytes:
        # if not data_url.startswith('data:image/jpg;base64,'):
        if not data_url.startswith('data:'):
            raise ValueError("Invalid data URL format")
        base64_data = data_url.split(',', 1)[1]
        return base64.b64decode(base64_data)
