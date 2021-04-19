import os
import sys
import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

'''
SAVE = 'saved_images'
if not os.path.exists(SAVE):
    os.mkdir(SAVE)
'''


class PolluteData:
    def __init__(self, x, y, intensity=120, ratio=1.0, radius=20, _type='Gaussian', hot_spot='red'):
        self.center = np.array([x, y])
        self.inten = intensity
        self.ratio = ratio
        self.radius = radius
        self.atk_type = _type
        self.hot_spot = hot_spot

    def gen_mask(self, shape):
        mask = np.zeros(shape[:2])
        if self.atk_type == 'Flaptop':
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (i-self.center[0]) ** 2 + (j-self.center[1]) ** 2 <= self.radius ** 2:
                        mask[i, j] = 1.0
        elif self.atk_type == 'Gaussian':
            gauss = self.gaussian()
            print(gauss[20,20])
            print(gauss[10,20])
            print(gauss[0,39])
            print(gauss[0,20])
            print(gauss[0,10])
            mask[self.center[0]-self.radius:self.center[0]+self.radius, self.center[1]-
                                                                        self.radius:self.center[1]+self.radius] = gauss
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if (i - self.center[0]) ** 2 + (j - self.center[1]) ** 2 >= self.radius ** 2:
                        mask[i, j] = 0.0
        else:
            pass
        return mask

    def gen_mark(self, shape):
        mark = np.ones(shape)
        if self.hot_spot == 'red':
            mark[:, :, 0] *= self.inten
            mark[:, :, 1:] *= 0
        elif self.hot_spot == 'white':
            mark[:, :, 0] *= self.inten * (255/255)
            mark[:, :, 1] *= self.inten * (105/255)
            mark[:, :, 2] *= self.inten * (180/255)
        else:
            pass
        return mark

    def gaussian(self):
        a, b = np.meshgrid(np.linspace(-1, 1, 2*self.radius), np.linspace(-1, 1, 2*self.radius))
        dst = np.sqrt(a * a + b * b)
        sigma = 0.6
        muu = 0.000
        gauss = np.exp(-((dst - muu) ** 2 / (2.0 * sigma ** 2)))
        return gauss

    def add_signal(self, image):
        X = np.zeros(image.shape, dtype='float')
        # deepcopy doesn't works for opencv data type 'Image'
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                X[i][j][0] = image[i][j][0]
                for k in range(1, 3):
                    X[i][j][k] = image[i][j][k]
                    if (i - self.center[0]) ** 2 + (j - self.center[1]) ** 2 <= self.radius ** 2:
                        X[i][j][k] *= self.ratio
        mask = self.gen_mask(X.shape)
        mark = self.gen_mark(X.shape)
        if self.hot_spot == 'red':
            X[:, :, 0] += mask * mark[:, :, 0]
        elif self.hot_spot == 'white':
            X[:, :, 0] += mask * mark[:, :, 0]
            X[:, :, 1] += mask * mark[:, :, 1]
            X[:, :, 2] += mask * mark[:, :, 2]

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                for k in range(3):
                    if X[i][j][k] > 255:
                        X[i][j][k] = 255
                    if X[i][j][k] < 0:
                        X[i][j][k] = 0
        return X.astype(np.uint8)

'''
print(X_red[120:130, 120:130])
# plt.imshow(X[...,::-1])
# plt.show()
print(type(X))
print(X_face.shape)
print(X_face)
save_path = 'saved_images/Ariel_Sharon_100.jpg'
cv2.imwrite(save_path, X[...,::-1], [int(cv2.IMWRITE_JPEG_QUALITY), 95])
# plt.imsave(文件名,X,format='png')
'''
