from otsu import highlight_by_Otsu
from PIL import Image

img_url = 'imgs/im_bl.jpg'
img = highlight_by_Otsu(img_url)
img.show()