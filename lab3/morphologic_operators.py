import numpy as np


def apply(img_pixel_matrix, structure_element, operation):
    for i in img_pixel_matrix:
        for j in i:
            if(j==255):
                j = 0
            else:
                j = 1   

    filtered_pixels_image = __apply_operator(img_pixel_matrix, structure_element, operation)
    return filtered_pixels_image


def erosion(pixel_mat, structure_matrix):
    b = structure_matrix
    sum_b = np.sum(b)
    counter = 0
    for i in range(pixel_mat):
        for j in range(pixel_mat[0]):
            if (pixel_mat[i][j] == b[i][j] == 1):
                counter += 1
    if (counter == sum_b):
        return True
    return False


# structure element is a tuple (B, S)
#              where: B - structure element matrix/binary digital image
#                     S - spetial point of structure element (x, y)
def __apply_operator(digital_image, structure_element, operation):
    if (type(digital_image[0][0]) == "tuple"):
        print("Error using 3 color image instead of 1")
        return
    if (type(structure_element) != "tuple"):
        print("Not valid structure element. Check if type of the provided structure element is tuple")
        return
    sample = digital_image.copy()
    res_image = np.zeros(len(digital_image), len(digital_image[0]))
    b, s = structure_element[0], structure_element[1]
    for row in range(len(res_image)-len(b)):
        for col in range(len(res_image[0]) - len(b[0])):
            res_image[row+s[0]][col+s[1]] = int( operation(sample[row:row+len(b)][col:col+len[b[0]]],   b))   # setting 1 or 0 into the spetial point

    return res_image
