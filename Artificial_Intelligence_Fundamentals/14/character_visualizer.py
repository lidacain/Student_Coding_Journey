import os
import sys

import cv2
import numpy as np

input_file = 'letter.data'

img_resize_factor = 12
start = 6
end = -1
height, width = 16, 8

with open(input_file, 'r') as f:
    for line in f.readlines():
        data = np.array([255 * float(x) for x in line.split('\t')[start:end]])

        img = np.resize(data, (height, width))

        img_scaled = cv2.resize(img, None, fx=img_resize_factor, fy=img_resize_factor)

        cv2.imshow('Image', img_scaled)

        c = cv2.waitKey()
        if c == 27:
            break