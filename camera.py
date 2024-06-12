import numpy as np
import cv2

class Camera():
    def __init__(self, height = 170, coordinates = (320, 320)):
        self.height = height
        self.x = coordinates[0]
        self.y = coordinates[1]

def get_coordinates(box, pallet):
    pass

def get_image_part(box, camera):
    if box.start_x <= camera.x and box.start_y <= camera.y:
        return 1
    elif box.start_x > camera.x and box.start_y < camera.y:
        return 2
    elif box.start_x >= camera.x and box.start_y >= camera.y:
        return 3
    return 4

def count_hypotenuse(box, pallet, camera):
    return np.sqrt(camera.height ** 2 + box)

def count_height(box, pallet):
    pass

def count_scale(box, pallet):
    scale_x = box.x_size / box.dx
    scale_y = box.y_size / box.dy
    return scale_x, scale_y

def count_distortion(box, pallet):
    pass

def count_position_3d(box, pallet):
    pass