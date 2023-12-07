from PIL import Image
import numpy as np
from morphologic_operators import apply, erosion, dilation, opening, closing

img_url = 'imgs/pixel_img.png'
img = Image.open(img_url)


structure_element = ([
    [0, 0, 0],
    [0, 1, 0],
    [0, 1, 0]    
], (1, 1))


pixels = [t[0] for t in list(img.getdata())]

pixel_matrix = np.array(pixels).reshape(img.height, img.width)
erosion_img = apply(pixel_matrix, structure_element, erosion)
print(erosion_img)
dilation_img = apply(pixel_matrix, structure_element, dilation)
print(dilation_img) 
opening_img = apply(pixel_matrix, structure_element, opening)
print(opening_img) 
closing_img = apply(pixel_matrix, structure_element, closing)
print(closing_img) 
erosion_img = Image.fromarray(erosion_img.astype('uint8'))
erosion_img.show()
dilation_img = Image.fromarray(dilation_img.astype('uint8'))
dilation_img.show()
opening_img = Image.fromarray(opening_img.astype('uint8'))
opening_img.show()
closing_img = Image.fromarray(closing_img.astype('uint8'))
closing_img.show()

img.show()