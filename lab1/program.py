from PIL import Image
import whb_conv
import matplotlib.pyplot as plt

img = Image.open("imgs/im2.jpg")
pixels = list(img.getdata())
img.putdata(whb_conv.conv(pixels))
pixels = list(img.getdata())
# img.show()

histogram = whb_conv.histogram_whb(pixels)
# plt.plot(histogram)
# plt.show()

prob = whb_conv.probabilities_of_lightness(histogram)

max_treshold = max(prob)
Imax = prob.index(max_treshold)
q1, q2, mu1, mu2 = [0]*Imax, [0]*Imax, [0]*Imax, [0]*Imax
gd1, gd2 = [0]*Imax, [0]*Imax #group despersion %n  / σ²

# step3 for each treshold:
def f(treshold):
    print("treshold: ", treshold)
    q1.append(sum(prob[:treshold]))
    q2.append(sum(prob[treshold+1:Imax]))
    if(q1[treshold]==0):return
    mu1.append(sum({i*prob[i]/q1[treshold] for i in range(treshold)}))
    mu2.append(sum({i*prob[i]/q2[treshold] for i in range(treshold+1,Imax)}))
    gd1.append(sum({
        (i-mu1[treshold])**2*prob[i]/q1[treshold] for i in range(treshold)
        }))
    gd2.append(sum({
        (i-mu2[treshold])**2*prob[i]/q2[treshold] for i in range(treshold+1, Imax)
        }))

for t in range(Imax):
    f(t)

print(
    "q1: ", q1,
    "q2: ", q2,
    "mu1: ", mu1,
    "mu2: ", mu2,
    "gd1: ", gd1,
    "gd2: ", gd2,
    "len: ", len(q1), len(q2), len(mu1), len(mu2) 
)

# t = max(probabilities[0], probabilities[255])

# q1 = sum(list[:t]) # =probabilities[0]
# q2 = sum(list[t:]) # =probabilities[255]
# μ1 = 0
# μ2 = 255

# # due to we process W/B there is only one 't' value
# def dispersion():
#     sum1 = 0
#     for i in range(t):
#         sum+= (i-μ1)**2*probabilities[i]/q1
#     sum2 = 0
#     for i in range(t, 256):
#         sum+= (i-μ2)**2*probabilities[i]/q2
#     return sum1, sum2

# si1, si2 = dispersion()
# si_w = q1*si1+q2*si2
# t_opt = 




# print(μ1, μ2)
# print(len(hist))


# width, height = img.size
# pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
# print(pixels)