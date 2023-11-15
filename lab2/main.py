from PIL import Image
import filters
import numpy as np

img_url = 'imgs/iguana.jpg'
img = Image.open(img_url)
# filtered_pixels_image = filters.apply_filter(img, filters.filter_gausian(7, 7))
# filtered_pixels_image = filters.apply_filter(img, [[0,0,0],[0,-1,0],[0,0,0]])
# filtered_pixels_image = filters.apply_filter(img, filters.filter_diagonal_movement(7, 7))
# filtered_pixels_image = filters.apply_filter(img, filters.filter_sharpening())
# filtered_pixels_image = filters.apply_filter(img, filters.filter_sobel_dy())
# filtered_pixels_image = filters.apply_filter(img, filters.filter_corners())
# filtered_pixels_image = filters.apply_filter(img, filters.filter_random())
filtered_pixels_image = filters.apply_filter_grad_magnitude(img)

filtered_img = img.copy()
filtered_img.putdata(filtered_pixels_image)
filtered_img.show()
# img.show()





