from MediaManager import MediaManager
from media.FileMediaManager import FileMediaManager
from media.RqMediaManager import RqMediaManager

png_bytes = FileMediaManager().file_read("static/dog.png")

rq_mgr = RqMediaManager()

png_url = rq_mgr.file_write("12345678", ".png", png_bytes, "image/png")

print(f'<html><img src="{png_url}"/></html>')

file_list = rq_mgr.file_list()

print(f'{file_list}')
