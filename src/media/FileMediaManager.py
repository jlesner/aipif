import base64

from ContextAware import ContextAware

class FileMediaManager(ContextAware):
        
    def binary_file_read(path:str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()
        
    def binary_file_write(path:str, data:bytes):
        with open(path, 'wb') as file:
            file.write(data)

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

# Testing
# data = ... # Some bytes of an image
# url = bytes_to_jpg_url(data)
# back_to_data = jpg_url_to_bytes(url)
# assert back_to_data == data

