import numpy as np
import skimage
import skimage.io
from scipy import sparse
from scipy.sparse.linalg import eigs,svds
import matplotlib.pyplot as plt
from time import *

#Tạo ma trận tương đồng đối xứng W
def generate_W(img):
    N = len(img)
    d = np.zeros((N, N), dtype=np.uint8)
    for i in range(N):
        d[i, :] = np.abs(img - img[i])
    W = np.exp(-np.power(d / np.max(d), 2))
    return W