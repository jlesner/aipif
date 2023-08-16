from MediaManager import MediaManager

png = MediaManager.binary_file_read("src/static/dog.png")

png_url = MediaManager.bytes_to_png_url(png)

print(f'<html><img src="{png_url}"/></html>')
