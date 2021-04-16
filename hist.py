from skimage import data
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import argparse

ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

img = plt.imread('D:/ThayHa/2f21b7f679dd8b83d2cc.jpg')

g_img = (rgb2gray(img)*256).astype('uint8')

plt.hist(g_img.ravel(), bins = 256)

plt.show()