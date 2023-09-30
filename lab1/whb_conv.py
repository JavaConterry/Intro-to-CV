




def IS_valid_pixels_list(pixels):
    print("ERROR?")
    print(type(pixels))
    if(type(pixels) is not list):
        print("A")
        return False
    if(len(pixels)==0):
        print("A")
        return False
    if(type(pixels[0][0]) is not int):
        print("A")
        return False
    print("data is valid")
    return True

def IS_whb(pixels):
    print("ERROR?")
    if(pixels[0][0] != pixels[0][1] or pixels[  0][0] != pixels[0][2]):
        print("A")
        return False
    print("data is Wh/B image")
    return True



# requires List type of pixels. Use list(img.getdata()), img -PIL Image obj
# returns new pixels in white/black format
def conv(pixels):
    if(IS_valid_pixels_list(pixels) is False):
        return
    converted = []
    for i in pixels:
        aver = int(sum(i)/3)
        converted.append((aver, aver, aver))
    return(converted)

# only for white black pixel set
# returns histogram as list
def histogram_whb(pixels):
    if(not IS_valid_pixels_list(pixels) and not IS_whb(pixels)):
        return
    
    histogram_counter = {i:0 for i in range(256)}
    for pixel in pixels:
        histogram_counter[pixel[0]] += 1
    histogram = histogram_counter.values()
    return histogram


# histogram should be of whb photo
def probabilities_of_lightness(histogram):
    probabilities = []
    s = sum(histogram)
    for h in histogram:
        probabilities.append(h/s)
    return probabilities
    
#t_opt - optimal treshold
#obj_tone= 'bl' or 'wh'
def mask(pixels, t_opt, obj_tone="bl"):
    if(not IS_valid_pixels_list(pixels) and not IS_whb(pixels)):
        return

    if(obj_tone=='bl'):
        mi_t, ma_t = 255, 0
    else:
        mi_t, ma_t = 0, 255
        
    for i in range(len(pixels)):
        mask_pixel_tone = (mi_t if pixels[i][0]<=t_opt else ma_t) 
        pixels[i] = (mask_pixel_tone,mask_pixel_tone,mask_pixel_tone)
    return pixels

#returns image pixels by provided mask
def img_from_mask(original_img_pixels, mask_pixels):
    if(not IS_valid_pixels_list(mask_pixels)):
        return
    if(len(mask_pixels) != len(original_img_pixels)):
        return

    new_original_img_pixels = original_img_pixels
    for i in range(len(mask_pixels)):
        if(mask_pixels[i][0]==0):
            new_original_img_pixels[i] = (255,255,255)

    return new_original_img_pixels