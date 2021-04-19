import numpy as np
import skimage
import skimage.io
from scipy import sparse
from scipy.sparse.linalg import eigs,svds
import matplotlib.pyplot as plt
import cv2
from time import *

#Tạo ma trận tương đồng đối xứng W
class Ncut(object):    
    def __init__(self, img):
        
        self.no_rows, self.no_cols, self.channel = img.shape
        self.N = self.no_rows * self.no_cols
        self.V_nodes = self.V_node_maker(img)
        self.X = self.X_maker()
        self.F = self.F_maker(img)
        # parameter for W clculate
        self.r = 2
        self.sigma_I = 4
        self.sigma_X = 6
        # Dense W,D
        self.W = self.W_maker()


    def V_node_maker(self, img):
        b,g,r = cv2.split(img)
        b = b.flatten()
        g = g.flatten()
        r = r.flatten()
        V_nodes = np.vstack((b,g))
        V_nodes = np.vstack((V_nodes,r))
        return V_nodes

    def X_maker(self):
        X_temp = np.arange(self.N)
        X_temp = X_temp.reshape((self.no_rows,self.no_cols))
        X_temp_rows = X_temp // self.no_rows
        X_temp_cols = (X_temp // self.no_cols).T
        X = np.zeros((self.N, 1, 2))
        X[:,:,0] = X_temp_rows.reshape(self.N,1)
        X[:,:,1] = X_temp_cols.reshape(self.N,1)
        
        return X

    def F_maker(self,img):
        if self.channel < 2:
            return self.gray_feature_maker(img)
        else:
            return self.color_img_feature_maker(img)

    def gray_feature_maker(self,img):
        print('need to ')

    def color_img_feature_maker(self,img):
        F = img.flatten().reshape((self.N,1,self.channel))
        F = F.astype('uint8')
       
        return F

    def W_maker(self):
        X = self.X.repeat(self.N,axis = 1)
        X_T = self.X.reshape((1,self.N,2)).repeat(self.N,axis = 0)
        diff_X = X - X_T
        diff_X = diff_X[:,:,0]**2 + diff_X[:,:,1]**2

        F = self.F.repeat(self.N,axis = 1)
        F_T = self.F.reshape((1,self.N,3)).repeat(self.N,axis = 0)
        diff_F = F - F_T
        diff_F = diff_F[:,:,0]**2 + diff_F[:,:,1]**2 + diff_F[:,:,2]**2

        W_map = diff_X < self.r**2 # valid map for W

        W = np.exp(-((diff_F / (self.sigma_I**2)) + (diff_X / (self.sigma_X**2))))
        print(W*W_map)
        return W * W_map 
if __name__ == '__main__':
    img = cv2.imread('C:/Users/Admin/HienNguyen/VietBao/Normalized-Cut/ncut/test.jpg', cv2.IMREAD_COLOR)
    cutter = Ncut(img).W_maker
    print(cutter)
    