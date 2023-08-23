from MediaManager import MediaManager
from media.FileMediaManager import FileMediaManager

png = FileMediaManager().binary_file_read("static/dog.png")

png_url = MediaManager().bytes_to_png_url(png)

print(f'<html><img src="{png_url}"/></html>')
