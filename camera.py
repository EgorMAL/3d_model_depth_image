import numpy as np
import cv2

class Camera():
    def __init__(self, height = 170, coordinates = (320, 320)):
        self.height = height
        self.x = coordinates[0]
        self.y = coordinates[1]
