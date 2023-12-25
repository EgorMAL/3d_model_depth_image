# import pyrealsense2 as rs
# import numpy as np
# import cv2


# # Преобразование кадра в numpy array
# color_image = cv2.imread("./3d20/9_Color.png")
# cv2.imshow('Original', color_image)
# # Преобразование в градации серого
# gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

# # Применяем размытие для уменьшения шума
# blurred = cv2.GaussianBlur(gray, (5, 7), 0)
# cv2.imshow('Blurred', blurred)
# # Обнаружение границ с помощью Canny
# edged = cv2.Canny(blurred, 30, 150)

# # Находим контуры на изображении
# contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# print(len(contours))
# # Рисуем контуры на оригинальном цветном изображении
# cv2.drawContours(color_image, contours, -1, (0, 255, 0), 2)

# # Показываем изображение
# cv2.imshow('Contours', color_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import numpy as np
import cv2
filename = './3d20/2_Color.png'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
dst = cv2.cornerHarris(blurred,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()