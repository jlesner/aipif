import base64

from ContextAware import ContextAware

class B64MediaManager(ContextAware):

    def bytes_to_png_url(data:bytes):
        return 'data:image/png;base64,' \
            + base64.b64encode(data).decode('utf-8')
    
    def bytes_to_jpg_url(data:bytes):
        return 'data:image/jpg;base64,' \
            + base64.b64encode(data).decode('utf-8')
        
    def binary_file_read(path:str):
        with open(path, 'rb') as file:
            return file.read()
        
    def binary_file_write(path:str, data:bytes):
        with open(path, 'wb') as file:
            file.write(data)
