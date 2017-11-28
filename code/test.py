import cv2
import numpy as np


d = np.zeros([10, 10], dtype=np.uint8)
d[4][5] = 1
d[2][8] = 1
y, x = d.nonzero()
print(a)