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

def get_diff(img1, img2, lower_bound=10, upper_bound=180):
    """Function returns difference between images i and i+1"""
    diff = img1 - img2

    mask = np.zeros_like(diff)
    mask[(diff >= lower_bound) & (diff <= upper_bound)] = 255

    return mask

def get_contour(img):
    """Function return contour of the new object from image."""
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    maxContour = contours[0]
    for contour in contours[1::]:
        # Searching max area of contours
        if cv2.contourArea(contour) > cv2.contourArea(maxContour):
            maxContour = contour

    return maxContour

def find_corners_coordinates(img):
    """Function returns all pixel which could be box's corners."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)

    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    dst = cv2.dilate(dst,None)

    img[dst>0.01*dst.max()]=[0,0,255]

    fragment_x,fragment_y = np.where(np.all(img==[0,0,255], axis=2))

    return (fragment_x, fragment_y)

def find_edges(img):
    """Function returns box's edges"""
    edge = cv2.Canny(img, 50, 150)
    contours, _ = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    cv2.imshow("Canny", img)

    return contours


# gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
