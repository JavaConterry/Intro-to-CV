from PIL import Image
import numpy as np
from morphologic_operators import apply, erosion

img_url = 'imgs/pixel_img.png'
img = Image.open(img_url)


structure_element = ([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]    
], (1, 1))


pixels = [t[0] for t in list(img.getdata())]

pixel_matrix = np.array(pixels).reshape(img.height, img.width)
filtered_img = apply(pixel_matrix, structure_element, erosion)
filtered_img = Image.fromarray(filtered_img.astype('uint8'))
filtered_img.show()