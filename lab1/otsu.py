from PIL import Image
import pixelprocessor as ppr
import matplotlib.pyplot as plt
import numpy as np

def highlight_by_Otsu(url='imgs/im_bl.jpg', show_mediatorial_res=False):
    img = Image.open(url)
    obj_tone = 'bl'
    pixels = list(img.getdata())
    img_whb= img.copy()
    new_pixels = ppr.conv(pixels)
    # if(obj_tone == 'wh'):
    #     new_pixels = ppr.invert_greyscale(new_pixels)
    img_whb.putdata(new_pixels)
    pixels = list(img_whb.getdata())
    if(show_mediatorial_res):
        img.show()

    histogram = ppr.histogram_bw(pixels)
    if(show_mediatorial_res):
        plt.plot(histogram)
        plt.show()

    prob = ppr.probabilities_of_lightness(histogram)

    max_treshold = max(prob)
    Imax = prob.index(max_treshold)
    q1, q2, mu1, mu2 = [0]*Imax, [0]*Imax, [0]*Imax, [0]*Imax
    gd1, gd2 = [0]*Imax, [0]*Imax #group despersion %n  / σ²
    total_disp = [0]*Imax

    def fill_variables(treshold):
        q1[treshold] = sum(prob[:treshold])
        q2[treshold] = sum(prob[treshold+1:Imax])
        if(q1[treshold]==0):return
        mu1[treshold] = sum({i*prob[i]/q1[treshold] for i in range(treshold)})
        mu2[treshold] = sum({i*prob[i]/q2[treshold] for i in range(treshold+1,Imax)})
        gd1[treshold] = sum({
            (i-mu1[treshold])**2*prob[i]/q1[treshold] for i in range(treshold)
            })
        gd2[treshold] = sum({
            (i-mu2[treshold])**2*prob[i]/q2[treshold] for i in range(treshold+1, Imax)
            })
        # total_disp[treshold] = q1[treshold]*gd1[treshold]+q2[treshold]*gd2[treshold]
        total_disp[treshold] = q1[treshold]*q2[treshold]*((mu1[treshold]-mu2[treshold])**2)

    for t in range(Imax):
        fill_variables(t)

    print(
        "q1: ", q1[:5], "\n",
        "q2: ", q2[:5], "\n",
        "mu1: ", mu1[:5], "\n",
        "mu2: ", mu2[:5], "\n",
        "gd1: ", gd1[:5], "\n",
        "gd2: ", gd2[:5], "\n",
        "total_disp: ", total_disp[:100], "\n",
        "len: ", len(q1), len(q2), len(mu1), len(mu2), len(total_disp), "\n",
        "Imax: ", Imax, "\n",
        "Full len (prob): ", len(prob)
    )

    t_opt = np.argmax(total_disp)
    print('t_opt: ', t_opt)

    masked_pixels = ppr.mask(pixels, t_opt, obj_tone=obj_tone)
    # if(obj_tone == 'wh'):
    #     masked_pixels = ppr.invert_greyscale(masked_pixels)
    mask_img = img_whb.copy()
    mask_img.putdata(masked_pixels)
    if(show_mediatorial_res):
        mask_img.show()

    new_img_from_mask_pixels = ppr.img_from_mask(list(img.getdata()), masked_pixels)
    result_img = img.copy()
    result_img.putdata(new_img_from_mask_pixels)
    if(show_mediatorial_res):
        result_img.show()
    return result_img
