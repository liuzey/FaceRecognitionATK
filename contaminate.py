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


def add_signal(Y, a, b, c, d, intensity, ratio):
    X = np.zeros(Y.shape, dtype='float')
    # deepcopy doesn't works for opencv data type 'Image'
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            for k in range(3):
                X[i][j][k] = Y[i][j][k]
    X_face = X[a:b, c:d, :]

    # If you try to use irregular pattern, try use index list like follows:
    # list1 = list(range(5,25))
    # list1.extend(list(range(45,65)))
    # for i in range(list1)

    for i in range(b-a):
        for j in range(d-c):
            # R + intensity
            for k in range(1):
                X_face[i][j][k] = X_face[i][j][k] + intensity
                if X_face[i][j][k]>= 255:
                    X_face[i][j][k] = 255
                if X_face[i][j][k]<= 0:
                    X_face[i][j][k] = 0
            # GB * ratio
            for t in range(1,3):
                X_face[i][j][t] = X_face[i][j][t]*ratio

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
