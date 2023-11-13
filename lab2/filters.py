import numpy

def filter_shift(right, bottom): #in case of left and top, use negative values
    filter_shift = [[0] * (abs(right)*2+1) for _ in range(abs(bottom)*2+1)]
    filter_shift[abs(bottom)+bottom][abs(right)+right]=1
    return filter_shift

def __palindrome(length):
    set_val = []
    for i in range(1, (length+1)// 2):
        set_val.append(i)
    if length % 2 == 0:
        set_val.extend(reversed(set_val))
    else:
        set_val.append(length // 2 +1)
        copy_rev = set_val.copy()
        copy_rev.reverse()
        set_val.extend(copy_rev[1:])
    print(set_val)
    return set_val

def filter_gausian(width, height): # numpy a little bit was used
    w = numpy.array(__palindrome(width))
    h = numpy.array(__palindrome(height)).reshape(-1, 1)
    
    gaus_mat = numpy.dot(w.reshape(-1, 1), h.reshape(1, -1))
    return gaus_mat

def filter_inverse(size):
    return [[0, 0, 0],[0, -1, 0],[0, 0, 0]]

def filter_diagonal_movement(width, height):
    filter = [[0]*height for i in range(width)]
    for i in range(height):
        for j in range(width):
            if(i==j): filter[i][j]=1
    return filter

def filter_sharpening():
    return [[0,-1,0],[-1,5,-1],[0,-1,0]]


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

    result_img = [(r, g, b) for r, g, b in zip(pixel_r_list, pixel_g_list, pixel_b_list)]
    return result_img


def __apply_filter_color(img, filter):
    if(type(img[0][0])=="tuple"):
        print("Error using 3 color image instead of 1")
        return
    img = list(img.copy())
    img_width = len(img[0])
    img_height = len(img)
    filter_width = len(filter[0])
    filter_height = len(filter)
    init_point_x = int((filter_width - 1) / 2)
    fin_point_x = int(img_width - filter_width - 1)
    init_point_y = int((filter_height - 1) / 2)
    fin_point_y = int(img_height - filter_height - 1)
    normalisation_sum_of_filter = abs(numpy.sum(filter))

    
    for row in range(init_point_y, fin_point_y):
        for col in range(init_point_x, fin_point_x):
            pixel_val = 0
            for k in range(filter_height):
                for l in range(filter_width):
                    pixel_val += img[row + l][col + k] * filter[l][k]
            img[row][col] = int(pixel_val / normalisation_sum_of_filter)
    min_p = numpy.min(numpy.array(img))
    print(min_p)
    #shift
    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j]+=abs(min_p)
    return img
# filter_shift = create_filter_shift(10, 20)
# print_filter(filter_shift)
