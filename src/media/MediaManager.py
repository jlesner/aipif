import base64

class MediaManager:

    def bytes_to_png_url(data:bytes):
        return 'data:image/png;base64,' \
            + base64.b64encode(data).decode('utf-8')
    
    def bytes_to_jpg_url(data:bytes):
        return 'data:image/jpg;base64,' \
            + base64.b64encode(data).decode('utf-8')
