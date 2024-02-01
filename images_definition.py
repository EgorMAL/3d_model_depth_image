import numpy as np
import cv2

def color_images_definition(img1_color, img2_color, img1_depth, img2_depth):
    gray1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

    depth1 = cv2.cvtColor(img1_depth, cv2.COLOR_BGR2GRAY)
    depth2 = cv2.cvtColor(img2_depth, cv2.COLOR_BGR2GRAY)

    depth = depth2 - depth1
    # Убираем тени
    smooth1 = cv2.GaussianBlur(gray1, (95,95), 0)
    smooth2 = cv2.GaussianBlur(gray2, (95,95), 0)

    division1 = cv2.divide(gray1, smooth1, scale=192)
    division2 = cv2.divide(gray2, smooth2, scale=192)

    # # Вычитание фонового изображения
    diff = cv2.absdiff(division2, division1)
    # diff = cv2.absdiff(gray2, gray1)
    # Применение пороговой обработки
    threshold = 35
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    # Нахождение контуров объектов
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Выделение объекта на втором изображении
    maxContour = contours[0]
    for contour in contours[1::]:
        # Searching max area of contours
        if cv2.contourArea(contour) > cv2.contourArea(maxContour):
            maxContour = contour

    (x, y, w, h) = cv2.boundingRect(maxContour)
    cv2.rectangle(img2_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Color diff", img2_color)

    cv2.rectangle(depth2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Depth diff", depth2)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # self.area = cv2.contourArea(maxContour)
    # self.startCoordinate = (x, y)
    # self.endCoordinate = (x + w, y + h)
img1_color = cv2.imread("./RealSense_Images/RealSense_Color_4.png")
img2_color = cv2.imread("./RealSense_Images/RealSense_Color_5.png")
img1_depth = cv2.imread("./RealSense_Images/RealSense_Depth_4.png")
img2_depth = cv2.imread("./RealSense_Images/RealSense_Depth_5.png")
color_images_definition(img1_color, img2_color, img1_depth, img2_depth)