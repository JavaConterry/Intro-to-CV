from PIL import Image
import filters
import numpy as np

img_url = 'imgs/iguana.jpg'
img = Image.open(img_url)
filtered_pixels_image = filters.apply_filter(img, filters.filter_gausian(7, 7))
# filtered_pixels_image = filters.apply_filter(img, [[0,0,0],[0,-1,0],[0,0,0]])


filtered_img = img.copy()
filtered_img.putdata(filtered_pixels_image)
filtered_img.show()
# img.show()





