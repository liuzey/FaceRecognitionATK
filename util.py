import numpy as np
import os.path
import sys
import time
import argparse
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from align import AlignDlib
from contaminate import add_signal


parser = argparse.ArgumentParser()
parser.add_argument("data", type=str, help='dataset type: adding pattern or T-shirt misdirect')
parser.add_argument("n", type=int, help='index of image to attack')
parser.add_argument("-i", "--inten", type=int, default=0, help='intensity added to R')
parser.add_argument("-r", "--ratio", type=float, default=1.0, help='ratio for decay in GB')
parser.add_argument("-a", type=int, default=0, help='starting pixels in x axis')
parser.add_argument("-b", type=int, default=-1, help='ending pixels in x axis')
parser.add_argument("-c", type=int, default=0, help='starting pixels in y axis')
parser.add_argument("-d", type=int, default=-1, help='ending pixels in y axis')
args = parser.parse_args()


class IdentityMetadata():
    def __init__(self, base, name, file):
        self.base = base
        self.name = name
        self.file = file

    def __repr__(self):
        return self.image_path()

    def image_path(self):
        return os.path.join(self.base, self.name, self.file)


def load_metadata(path):
    metadata = []
    for i in sorted(os.listdir(path)):
        for f in sorted(os.listdir(os.path.join(path, i))):
            ext = os.path.splitext(f)[1]
            if ext == '.jpg' or ext == '.jpeg':
                metadata.append(IdentityMetadata(path, i, f))
    return np.array(metadata)


metadata = load_metadata(args.data)


def load_image(path):
    img = cv2.imread(path, 1)
    contaminated_img = add_signal(img[..., ::-1], args.a, args.b, args.c, args.d, args.inten, args.ratio)
    return contaminated_img


# Load alignment model
alignment = AlignDlib('models/landmarks.dat')

target = load_image(metadata[args.n].image_path())

# Detect face and return bounding box
bb = alignment.getLargestFaceBoundingBox(target)

# Transform image using specified face landmark indices and crop image to 96x96
tg_aligned = alignment.align(96, target, bb, landmarkIndices=AlignDlib.OUTER_EYES_AND_NOSE)

# Show original image
plt.subplot(131)
plt.imshow(target)

# Show original image with bounding box
plt.subplot(132)
plt.imshow(target)
plt.gca().add_patch(patches.Rectangle((bb.left(), bb.top()), bb.width(), bb.height(), fill=False, color='red'))

# Show aligned image
plt.subplot(133)
plt.imshow(tg_aligned)
plt.show()