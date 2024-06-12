"""Pallet class"""
import cv2

class Pallet():
    """Pallet class describes pallet"""
    def __init__(self, image_path = './RealSense_Images/Color_1.png', x=75, y=75):
        self.size = (x, y)
        self.image_path = image_path
        self.top_left_coordinate = (64, 153)
        self.top_right_coordinate = (76, 502)
        self.bottom_left_coordinate = (416, 144)
        self.bottom_right_coordinate = (421, 492)

    def find_bounding_box(self):
        """Function for changing pallet's corners color."""
        img = cv2.imread(self.image_path)
        img[240,320] = (0,0,255)
        img[64,153] = (0,0,255) # 1
        img[76,502] = (0,0,255) # 2
        img[421,492] = (0,0,255) # 3
        img[416,144] = (0,0,255) # 4
        cv2.imshow('Pallet', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_dx(self):
        """Returns number of pixels between top left and bottom right corners by X"""
        return self.bottom_right_coordinate[0] - self.top_left_coordinate[0]

    def get_dy(self):
        """Returns number of pixels between top left and bottom right corners by Y"""
        return self.bottom_right_coordinate[1] - self.top_left_coordinate[1]
