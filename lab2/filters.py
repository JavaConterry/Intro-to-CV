import numpy
import random
import math
# from numba import njit




def __palindrome(length):
    set_val = []
    for i in range(1, (length+1) // 2):
        set_val.append(i)
    if length % 2 == 0:
        set_val.extend(reversed(set_val))
    else:
        set_val.append(length // 2 + 1)
        copy_rev = set_val.copy()
        copy_rev.reverse()
        set_val.extend(copy_rev[1:])
    print(set_val)
    return set_val

def filter_shift(right, bottom):  # in case of left and top, use negative values
    filter_shift = numpy.zeros((right, bottom))
    filter_shift[right-1, bottom-1] = 1
    return filter_shift


def filter_gausian(width, height):  # numpy a little bit was used
    w = numpy.array(__palindrome(width))
    h = numpy.array(__palindrome(height)).reshape(-1, 1)

    gaus_mat = numpy.dot(w.reshape(-1, 1), h.reshape(1, -1))
    return gaus_mat


def filter_inverse(size):
    return [[0, 0, 0], [0, -1, 0], [0, 0, 0]]


def filter_diagonal_movement(width, height):
    filter = [[0]*height for i in range(width)]
    for i in range(height):
        for j in range(width):
            if (i == j):
                filter[i][j] = 1
    return filter


def filter_sharpening():
    return [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]


def filter_sobel_dy():
    return [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]


def filter_sobel_dx():
    return [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]


def filter_corners():
    return [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]


def filter_random():
    return [[random.randint(-9, 9), random.randint(-9, 9), random.randint(-9, 9)], [random.randint(-9, 9), random.randint(-9, 9), random.randint(-9, 9)], [random.randint(-9, 9), random.randint(-9, 9), random.randint(-9, 9)]]


def __filter_grad_magnitude(img):
    img_gaus = __apply_filter_color(img, filter_gausian(3, 3))
    img_gaus_dx = __apply_filter_color(img_gaus, filter_sobel_dx())
    img_gaus_dy = __apply_filter_color(img_gaus, filter_sobel_dy())
    img_magn = img.copy()
    for i in range(len(img_magn)):
        for j in range(len(img_magn[0])):
            img_magn[i][j] = math.sqrt(
                math.pow(img_gaus_dx[i][j], 2)+math.pow(img_gaus_dy[i][j], 2))
    return img_magn


def apply_filter_grad_magnitude(img):
    red_pixels = [pixel[0] for pixel in img.getdata()]
    green_pixels = [pixel[1] for pixel in img.getdata()]
    blue_pixels = [pixel[2] for pixel in img.getdata()]

    # filtered_pixels_image = filters.apply_filter(pixels_img, filters.filter_shift(200, 300))
    pixel_r_matrix = numpy.array(red_pixels).reshape(img.height, img.width)
    pixel_g_matrix = numpy.array(green_pixels).reshape(img.height, img.width)
    pixel_b_matrix = numpy.array(blue_pixels).reshape(img.height, img.width)

    filtered_r_pixels_image = __filter_grad_magnitude(pixel_r_matrix)
    filtered_g_pixels_image = __filter_grad_magnitude(pixel_g_matrix)
    filtered_b_pixels_image = __filter_grad_magnitude(pixel_b_matrix)

    pixel_r_list = [pixel for row in filtered_r_pixels_image for pixel in row]
    pixel_g_list = [pixel for row in filtered_g_pixels_image for pixel in row]
    pixel_b_list = [pixel for row in filtered_b_pixels_image for pixel in row]

    result_img = [(r, g, b) for r, g, b in zip(
        pixel_r_list, pixel_g_list, pixel_b_list)]
    return result_img


# @njit(nogil=True)
def apply_filter(img, filter):
    red_pixels = [pixel[0] for pixel in img.getdata()]
    green_pixels = [pixel[1] for pixel in img.getdata()]
    blue_pixels = [pixel[2] for pixel in img.getdata()]

    # filtered_pixels_image = filters.apply_filter(pixels_img, filters.filter_shift(200, 300))
    pixel_r_matrix = numpy.array(red_pixels).reshape(img.height, img.width)
    pixel_g_matrix = numpy.array(green_pixels).reshape(img.height, img.width)
    pixel_b_matrix = numpy.array(blue_pixels).reshape(img.height, img.width)

    filtered_r_pixels_image = __apply_filter_color(pixel_r_matrix, filter)
    filtered_g_pixels_image = __apply_filter_color(pixel_g_matrix, filter)
    filtered_b_pixels_image = __apply_filter_color(pixel_b_matrix, filter)

    pixel_r_list = [pixel for row in filtered_r_pixels_image for pixel in row]
    pixel_g_list = [pixel for row in filtered_g_pixels_image for pixel in row]
    pixel_b_list = [pixel for row in filtered_b_pixels_image for pixel in row]

    result_img = [(r, g, b) for r, g, b in zip(
        pixel_r_list, pixel_g_list, pixel_b_list)]
    return result_img


def __rescale(img, min_p, max_p):
    m = img.copy()
    scale = abs(256/(max_p-min_p))
    for row in range(len(m)):
        for col in range(len(m[0])):
            m[row][col] = m[row][col] * scale
    return m


def __shift(img, min_p):
    m = img.copy()
    for i in range(len(m)):
        for j in range(len(m[0])):
            m[i][j] += abs(min_p)
    return m


def __clip(img):
    m = img.copy()
    for i in range(len(m)):
        for j in range(len(m[0])):
            if (img[i][j] > 255):
                img[i][j] = 255
            else:
                if (img[i][j] < 0):
                    img[i][j] = 0
    return m


def __extend_img_by_zeros(img, filter_size):
    img_h, img_w = len(img), len(img[0])
    filter_h, filter_w = filter_size
    extend_height = filter_h - 1
    extend_width = filter_w - 1
    extended_img = [[0] * (img_w + extend_width)
                    for _ in range(img_h + extend_height)]

    for i in range(img_h):
        for j in range(img_w):
            extended_img[i][j] = img[i][j]

    return extended_img


def __deextend_img(img, filter_size):
    filter_h, filter_w = filter_size
    deextended_height = len(img) - filter_h + 1
    deextended_width = len(img[0]) - filter_w + 1
    deextended_img = [[0] * deextended_width for _ in range(deextended_height)]
    for i in range(deextended_height):
        for j in range(deextended_width):
            deextended_img[i][j] = img[i][j]
    return deextended_img


def __apply_filter_color(img, filter):
    if (type(img[0][0]) == "tuple"):
        print("Error using 3 color image instead of 1")
        return
    img = list(img.copy())
    img_width = len(img[0])
    img_height = len(img)
    filter_width = len(filter[0])
    filter_height = len(filter)
    init_point_x = int((filter_width - 1) / 2 - 1)
    fin_point_x = int(img_width)
    init_point_y = int((filter_height - 1) / 2 - 1)
    fin_point_y = int(img_height)
    normalisation_sum_of_filter = abs(numpy.sum(filter))
    img = __extend_img_by_zeros(img, (filter_height, filter_width))

    for row in range(init_point_y, fin_point_y):
        for col in range(init_point_x, fin_point_x):
            pixel_val = 0
            for k in range(filter_height):
                for l in range(filter_width):
                    pixel_val += img[row + k][col + l] * filter[k][l] #l, k => k, l
            if (normalisation_sum_of_filter != 0):
                img[row][col] = int(pixel_val / normalisation_sum_of_filter)
            else:
                img[row][col] = int(pixel_val)
    # scaling
    # min_p = numpy.min(numpy.array(img))
    # max_p = numpy.max(numpy.array(img))
    # print("Before scaling and shifting")
    # print(min_p, " ", max_p)
    # img = __rescale(img, min_p, max_p)
    # #shifting
    # min_p = numpy.min(numpy.array(img))
    # img = __shift(img, min_p)
    # min_p = numpy.min(numpy.array(img))
    # max_p = numpy.max(numpy.array(img))
    # print("After scaling and shifting")
    # print(min_p, " ", max_p)  #    <-------img after process requires a Histogram equalization. Its not made on a course yet.
    img = __clip(img)
    img = __deextend_img(img, (filter_height, filter_width))
    return img
