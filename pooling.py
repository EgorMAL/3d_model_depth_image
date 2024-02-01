import numpy as np
import cv2

def pooling(img, step):
    for i in range(0, 480, step):
        for j in range(0, 640, step):
            min_value = img[i:i+step, j:j+step].max()
            img[i:i+step, j:j+step] = min_value
    return img

start1_img = cv2.cvtColor(cv2.imread("./RealSense_Images/RealSense_Depth_4.png"), cv2.COLOR_BGR2GRAY)
end1_img= pooling(start1_img.copy(), 2)

cv2.imshow("First1", start1_img)
cv2.imshow("Second1", end1_img)

start2_img = cv2.cvtColor(cv2.imread("./RealSense_Images/RealSense_Depth_5.png"), cv2.COLOR_BGR2GRAY)
end2_img= pooling(start2_img.copy(), 2)

cv2.imshow("First", start2_img)
cv2.imshow("Second", end2_img)

diff = end2_img - end1_img
cv2.imshow("Diff", diff)

lower_bound = 10
upper_bound = 200

# Создаем маску
mask = np.zeros_like(diff)  # Инициализируем маску нулями (черным цветом)
mask[(diff >= lower_bound) & (diff <= upper_bound)] = 255  # Устанавливаем белый цвет для пикселей внутри границ

cv2.imshow('Masked', mask)

pooled_mask = pooling(mask.copy(), 2)
cv2.imshow("Final", pooled_mask)

contours, _ = cv2.findContours(pooled_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Выделение объекта на втором изображении
maxContour = contours[0]
for contour in contours[1::]:
    # Searching max area of contours
    if cv2.contourArea(contour) > cv2.contourArea(maxContour):
        maxContour = contour

(x, y, w, h) = cv2.boundingRect(maxContour)
cv2.rectangle(start2_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Contour", start2_img)

color_img = cv2.imread("./RealSense_Images/RealSense_Color_5.png")
cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Contour color", color_img)

cv2.waitKey(0)
cv2.destroyAllWindows()