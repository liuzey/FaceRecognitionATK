import numpy as np
import os.path
import sys
import time
import argparse
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from align import AlignDlib
import contaminate_c


parser = argparse.ArgumentParser()
parser.add_argument("data", type=str, help='dataset type: adding pattern or T-shirt misdirect')
parser.add_argument("n", type=int, help='index of image to attack')
parser.add_argument("-i", type=int, default=0, help='intensity added to R')
parser.add_argument("-r", type=float, default=1.0, help='ratio for decay in GB')
parser.add_argument("-x", type=int, default=125, help='pattern center in x axis.')
parser.add_argument("-y", type=int, default=125, help='pattern center in y axis.')
parser.add_argument("-d", type=int, default=20, help='pattern radius.')
parser.add_argument("-t", type=str, default='Gaussian', help='type of power density: flattop or Gaussian.')
parser.add_argument("-hs", type=str, default='red', help='whether red or white in overexposing areas.')
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
    return img


# Load alignment model
alignment = AlignDlib('models/landmarks.dat')
img = load_image(metadata[args.n].image_path())
pollution = contaminate_c.PolluteData(args.x, args.y, intensity=args.i, ratio=args.r, radius=args.d,
                                    _type=args.t, hot_spot=args.hs)
target = pollution.add_signal(img[..., ::-1])

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