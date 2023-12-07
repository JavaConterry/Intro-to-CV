import numpy as np


def apply(img_pixel_matrix, structure_element, operation):
    img_pixel_matrix = np.where(img_pixel_matrix == 255, 0, 1)

    filtered_pixels_image = __apply_operator(
        img_pixel_matrix, structure_element, operation)

    filtered_pixels_image = np.where(filtered_pixels_image == 1, 0, 255)

    return filtered_pixels_image


# Defining wheather it is HIT FIT or MISS
def detect_pattern(pixel_mat, structure_matrix):
    b = structure_matrix
    sum_b = np.sum(b)
    counter = 0
    for i in range(len(pixel_mat)):
        for j in range(len(pixel_mat[0])):
            if (pixel_mat[i][j] == b[i][j] == 1):
                counter += 1
    if (counter == sum_b):
        return "FIT"
    elif (counter > 0):
        print("HIT")
        return "HIT"
    else:
        return "MISS"
    return


# operation
def erosion(pixel_mat, structure_matrix):
    return 1 if detect_pattern(pixel_mat, structure_matrix) == "FIT" else 0


# operation
def dilation(pixel_mat, structure_matrix):
    return 1 if detect_pattern(pixel_mat, structure_matrix) != "MISS" else 0

# operation


def opening():
    return

# operation


def closing():
    return


# structure element is a tuple (B, S)
#              where: B - structure element matrix/binary digital image
#                     S - spetial point of structure element (x, y)
def __apply_operator(digital_image, structure_element, operation):
    if (type(digital_image[0][0]) == "tuple"):
        print("Error using 3 color space image instead of binary")
        return
    if (type(structure_element) != tuple):
        print("Not valid structure element")
        return

    if (operation.__name__ != "opening" and operation.__name__ != "closing"):
        sample = digital_image.copy()
        res_image = sample.copy()
        b, s = structure_element[0], structure_element[1]
        for row in range(len(res_image)-len(b)):
            for col in range(len(res_image[0]) - len(b[0])):
                res_image[row+s[0]][col+s[1]
                                    ] = operation(sample[row:row+len(b), col:col+len(b[0])],   b)

    elif (operation.__name__ == "opening"):
        img_after_dilation = __apply_operator(
            digital_image, structure_element, dilation)
        res_image = __apply_operator(
            img_after_dilation, structure_element, erosion)
    elif (operation.__name__ == "closing"):
        img_after_erosion = __apply_operator(
            digital_image, structure_element, erosion)
        res_image = __apply_operator(
            img_after_erosion, structure_element, dilation)

    return res_image
