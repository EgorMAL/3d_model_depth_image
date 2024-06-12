# from operator import itemgetter
# from glob import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('./RealSense_Images/Color_3.png')

pts1 = np.float32([[120,30], [550,30], [120,400], [550,400]])

pts2 = np.float32([[0,0],[400, 0], [0, 400],[400, 400]])

# Apply Perspective Transform Algorithm
matrix = cv2.getPerspectiveTransform(pts1, pts2)
result = cv2.warpPerspective(img, matrix, (400, 400))

img[64,153] = (0,0,255) # 1
img[76,502] = (0,0,255) # 2
img[421,492] = (0,0,255) # 3
img[416,144] = (0,0,255) # 4
# Wrap the transformed image
cv2.imshow('frame', img) # Initial Capture
cv2.imshow('frame1', result) # Transformed Capture

cv2.waitKey(0)
cv2.destroyAllWindows()



