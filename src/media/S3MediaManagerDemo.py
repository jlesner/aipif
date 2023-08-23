from MediaManager import MediaManager
from media.FileMediaManager import FileMediaManager
from media.S3MediaManager import S3MediaManager

png_bytes = FileMediaManager().file_read("static/dog.png")

png_url = S3MediaManager().file_write("dog.png", png_bytes)

print(f'<html><img src="{png_url}"/></html>')

file_list = S3MediaManager().file_list()

file_list = S3MediaManager().file_list("media/")

print(f'{file_list}')
