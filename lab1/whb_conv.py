




def IS_valid_pixels_list(pixels):
    if(type(pixels) is not list):
        return False
    if(len(pixels)==0):
        return False
    if(type(pixels[0]) is not int):
        return False
    return True

def IS_whb(pixels):
    if(pixels[0][0] != pixels[0][1] or pixels[  0][0] != pixels[0][2]):
        return False
    return True



# requires List type of pixels. Use list(img.getdata()), img -PIL Image obj
# returns new pixels in white/black format
def conv(pixels):
    if(IS_valid_pixels_list is False):
        return
    converted = []
    for i in pixels:
        aver = int(sum(i)/3)
        converted.append((aver, aver, aver))
    return(converted)

# only for white black pixel set
# returns histogram as list
def histogram_whb(pixels):
    if(not IS_valid_pixels_list and not IS_whb):
        return
    
    histogram_counter = {i:0 for i in range(256)}
    for pixel in pixels:
        histogram_counter[pixel[0]] += 1
    histogram = histogram_counter.values()
    return histogram


# histogram should be of whb photo
def probabilities_of_lightness(histogram):
    if(not IS_valid_pixels_list and not IS_whb):
        return

    probabilities = []
    s = sum(histogram)
    for h in histogram:
        probabilities.append(h/s)
    return probabilities
    