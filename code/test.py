import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_operations.draw_lane import DrawLaneOperation

d = DrawLaneOperation(1280, 720)
bgr_frame = cv2.imread("./bird_view.png")
gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
binary = np.zeros_like(gray)
binary[gray == 255] = 1
r = d.execute(binary)

plt.imshow(r, cmap="gray")
plt.show()
