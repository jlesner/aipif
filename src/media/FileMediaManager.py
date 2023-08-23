import base64

from common.ContextAware import ContextAware

class FileMediaManager(ContextAware):
        
    def file_read(self, path:str) -> bytes:
        with open(path, 'rb') as file:
            return file.read()
        
    def file_write(self, path:str, data:bytes):
        with open(path, 'wb') as file:
            file.write(data)

# Testing
# data = ... # Some bytes of an image
# url = bytes_to_jpg_url(data)
# back_to_data = jpg_url_to_bytes(url)
# assert back_to_data == data

