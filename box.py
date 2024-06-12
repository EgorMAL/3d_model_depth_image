"""Box class"""
import cv2
from pallet import Pallet

class Box():
    """Class which describes objects on pallet."""
    def __init__ (self, box_id, x, y, z, image_path):
        self.id = box_id
        self.size = [x, y, z]
        self.image_path = image_path
        self.start_point = [None, None, None]
        self.d = [None, None, None]
        self.coordinates = [None, None]
        self.area = None
        self.under_box_id = None

    def find_box_start_point_3d(self, pallet: Pallet, queue):
        """Поиск стартовой точки для отрисовки (x и y переставлены местами)"""
        self.start_point[0] = self.coordinates[0][1] / 361 * pallet.size[0] * 0.01
        self.start_point[1] = self.coordinates[0][0] / 349 * pallet.size[0] * 0.01
        if self.under_box_id == -1:
            self.start_point[2] = 0
        else:
            for box in queue:
                if self.under_box_id == box.id:
                    self.start_point[2] = box.size[2] * 0.01

    def find_box_sizes_in_3d(self):
        """Поиск сторон для отрисовки (x и y переставлены местами)"""
        self.d[0] = round(float(self.size[1]) * 0.01, 4)
        self.d[1] = round(float(self.size[0]) * 0.01, 4)
        self.d[2] = round(float(self.size[2]) * 0.01, 4)
        print(self.d)

    def find_box_axes(self, pallet: Pallet):
        """Поиск настоящей ориентации сторон коробки при укладке
        (плоскость, которой положили на паллет)"""

        # Процентное соотношение сторон коробки к сторонам паллета,
        # подразумевается, что паллет квадратный
        percent_x = self.size[0] / pallet.size[0]
        percent_y = self.size[1] / pallet.size[0]
        percent_z = self.size[2] / pallet.size[0]

        # Процентное соотношение разницы координат коробки к разнице координат паллета
        percent_coordinate_x = (self.coordinates[1][0] - self.coordinates[0][0]) / 349
        percent_coordinate_y = (self.coordinates[1][1] - self.coordinates[0][1]) / 361

        # Стартовые размеры коробки без учета ориентации сторон
        real_x, real_y, real_z = self.size[0], self.size[1], self.size[2]

        if abs(percent_x - percent_coordinate_x) > abs(percent_y - percent_coordinate_x):
            real_x, real_y, real_z = real_y, real_x, real_z
            percent_x, percent_y, percent_z = percent_y, percent_x, percent_z
            if abs(percent_x - percent_coordinate_x) > abs(percent_z - percent_coordinate_x):
                real_x, real_y, real_z = real_z, real_y, real_x
                percent_x, percent_y, percent_z = percent_z, percent_y, percent_x

        if abs(percent_y - percent_coordinate_y) > abs(percent_z - percent_coordinate_y):
            real_x, real_y, real_z = real_x, real_z, real_y
            percent_x, percent_y, percent_z = percent_x, percent_z, percent_y
            if abs(percent_x - percent_coordinate_y) > abs(percent_y - percent_coordinate_y):
                real_x, real_y, real_z = real_y, real_x, real_z
                percent_x, percent_y, percent_z = percent_z, percent_y, percent_x

        if abs(percent_x - percent_coordinate_x) > abs(percent_z - percent_coordinate_x):
            real_x, real_y, real_z = real_z, real_y, real_x

        self.size[0] = real_x
        self.size[1] = real_y
        self.size[2] = real_z


    def find_under_box_id(self, packer, last_box_queue_number):
        """Поиск коробки внизу, если коробка есть, присваиваем id коробки в атрибут underBoxId,
        если нет, то присваиваем -1 в тот же атрибут"""

        under_box_id = -1
        max_interception = 0

        for box in packer.queue[1:last_box_queue_number]:
            # Левый верхний
            if (self.coordinates[0][0] > box.coordinates[0][0] and
                self.coordinates[0][1] > box.coordinates[0][1] and
                self.coordinates[0][0] < box.coordinates[1][0] and
                self.coordinates[0][1] < box.coordinates[1][1]):

                intersection_area = (
                    (box.coordinates[1][0] - self.coordinates[0][0]) *
                    (box.coordinates[1][1] - self.coordinates[0][1])
                )

                iou = intersection_area / float(self.area + box.area - intersection_area)

                if abs(iou) > 1:
                    if abs(iou) > max_interception:
                        max_interception = abs(iou)
                        under_box_id = box.id

            # Правый верхний
            if (self.coordinates[1][0] > box.coordinates[0][0] and
                self.coordinates[0][1] > box.coordinates[0][1] and
                self.coordinates[1][0] < box.coordinates[1][0] and
                self.coordinates[0][1] < box.coordinates[1][1]):

                intersection_area = (
                    (self.coordinates[1][0] - box.coordinates[0][0]) *
                    (box.coordinates[1][1] - self.coordinates[0][1])
                )

                iou = intersection_area / float(self.area + box.area - intersection_area)

                if abs(iou) > 1:
                    if abs(iou) > max_interception:
                        max_interception = abs(iou)
                        under_box_id = box.id

            # Левый нижний
            if (self.coordinates[0][0] > box.coordinates[0][0] and
                self.coordinates[1][1] > box.coordinates[0][1] and
                self.coordinates[0][0] < box.coordinates[1][0] and
                self.coordinates[1][1] < box.coordinates[1][1]):

                intersection_area = (
                    (box.coordinates[1][0] - self.coordinates[0][0]) *
                    (self.coordinates[1][1] - box.coordinates[0][1])
                )

                iou = intersection_area / float(self.area + box.area - intersection_area)

                if abs(iou) > 1:
                    if abs(iou) > max_interception:
                        max_interception = abs(iou)
                        under_box_id = box.id

            # Правый нижний
            if (self.coordinates[1][0] > box.coordinates[0][0] and
                self.coordinates[1][1] > box.coordinates[0][1] and
                self.coordinates[1][0] < box.coordinates[1][0] and
                self.coordinates[1][1] < box.coordinates[1][1]):

                intersection_area = (
                    (self.coordinates[1][0] - box.coordinates[0][0]) *
                    (self.coordinates[1][1] - box.coordinates[0][1])
                )

                iou = intersection_area / float(self.area + box.area - intersection_area)

                if abs(iou) > 1:
                    if abs(iou) > max_interception:
                        max_interception = abs(iou)
                        under_box_id = box.id

        self.under_box_id = under_box_id

    def get_bounding_box_coordinates(self, previousObject, pallet: Pallet):
        """Поиск координат контура новой коробки"""
        # Загрузка изображений
        image1 = cv2.imread(self.image_path)
        image2 = cv2.imread(previousObject.image_path)

        image1 = image1[pallet.top_left_coordinate[0]:pallet.bottom_right_coordinate[0],
                        pallet.top_left_coordinate[1]:pallet.bottom_right_coordinate[1]]
        image2 = image2[pallet.top_left_coordinate[0]:pallet.bottom_right_coordinate[0],
                        pallet.top_left_coordinate[1]:pallet.bottom_right_coordinate[1]]
        # Преобразование изображений в оттенки серого
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

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
        max_contour = contours[0]
        for contour in contours[1::]:
            # Searching max area of contours
            if cv2.contourArea(contour) > cv2.contourArea(max_contour):
                max_contour = contour

        (x, y, w, h) = cv2.boundingRect(max_contour)
        cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        self.area = cv2.contourArea(max_contour)
        self.coordinates[0] = (x, y)
        self.coordinates[1] = (x + w, y + h)

    def prepare_image():
        pass