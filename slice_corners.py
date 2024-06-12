"""Functions for image preprocessing"""
import numpy as np
import cv2

def pooling(img, step):
    """Min pooling operation. It helps to remove image distortion."""
    for i in range(0, 480, step):
        for j in range(0, 640, step):
            min_value = img[i:i+step, j:j+step].max()
            img[i:i+step, j:j+step] = min_value
    return img

for i in range(0, 31):
    start1_img = cv2.cvtColor(cv2.imread(f"./RealSense_Images/Depth_{i}.png"),
                              cv2.COLOR_BGR2GRAY)
    end1_img= pooling(start1_img.copy(), 2)
    start2_img = cv2.cvtColor(cv2.imread(f"./RealSense_Images/Depth_{i + 1}.png"),
                              cv2.COLOR_BGR2GRAY)
    end2_img= pooling(start2_img.copy(), 2)

    diff = end2_img - end1_img

    lower_bound = 10
    upper_bound = 180

    # Создаем маску
    mask = np.zeros_like(diff)  # Инициализируем маску нулями (черным цветом)
    mask[(diff >= lower_bound) & (diff <= upper_bound)] = 255  # Устанавливаем белый цвет для пикселей внутри границ

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

    color_img = cv2.imread(f"./RealSense_Images/Color_{i + 1}.png")
    # cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow("Contour color", color_img)

    fragment = color_img[y:y+h, x:x+w].copy()
    gray = cv2.cvtColor(fragment, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image.
    fragment[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('fragment', fragment)

    canny_fragment = color_img[y:y+h, x:x+w].copy()
    edge = cv2.Canny(canny_fragment, 50, 150)
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(canny_fragment, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Canny", canny_fragment)

    cv2.rectangle(color_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Contour color", color_img)

    fragment_x,fragment_y = np.where(np.all(fragment==[0,0,255], axis=2))

    for fy, fx in zip(fragment_x,fragment_y):
        color_img[y + fy, x + fx] = [255, 0, 0]
    cv2.imshow('dst',color_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
