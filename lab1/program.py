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

for t in range(Imax):
    f(t)

print(
    "q1: ", q1[:5], "\n",
    "q2: ", q2[:5], "\n",
    "mu1: ", mu1[:5], "\n",
    "mu2: ", mu2[:5], "\n",
    "gd1: ", gd1[:5], "\n",
    "gd2: ", gd2[:5], "\n",
    "len: ", len(q1), len(q2), len(mu1), len(mu2), "\n",
    "Imax: ", Imax, "\n",
    "Full len (prob): ", len(prob)
)


