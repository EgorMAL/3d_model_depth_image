# import numpy as np
# import cv2

# import numpy as np
# import cv2

# # Создаем массив размера (480, 640) с числами от 0.0 до 1.4
# array = np.linspace(0.0, 1.4, 480*640).reshape((480, 640)).astype(np.float64)
# print(array.shape)
# # Сохраняем изображение
# output_path = "array_image.png"
# cv2.imwrite(output_path, array * 255)  # Умножаем на 255 для корректного отображения в формате изображения

# cv2.imshow("Array as Image", array)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import numpy as np
import cv2

# # Создаем массив размера (480, 640), заполненный нулями (черный цвет)
# array = np.zeros((480, 640), dtype=np.float64)

# # Определяем размеры и положение центрального белого прямоугольника
# rect_height = 240  # Высота прямоугольника
# rect_width = 320   # Ширина прямоугольника
# start_y = (480 - rect_height) // 2  # Начальная координата y для прямоугольника
# start_x = (640 - rect_width) // 2   # Начальная координата x для прямоугольника

# # Заполняем прямоугольник белым цветом
# array[start_y:start_y + rect_height, start_x:start_x + rect_width] = 0.2
# # Сохраняем изображение
# output_path = "centered_rectangle_image.png"
# cv2.imwrite(output_path, array * 255)  # Умножаем на 255 для правильного отображения


image = cv2.imread("centered_rectangle_image.png")

blurred = cv2.GaussianBlur(image, (1, 1), 0)

# dst = cv2.cornerHarris(blurred,2,3,0.04)
# dst = cv2.dilate(dst,None)
# color_image[dst>0.01*dst.max()]=[0,0,255]
# Обнаружение границ с помощью Canny
edged = cv2.Canny(blurred, 30, 150)

# Находим контуры на изображении
contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на оригинальном цветном изображении
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Показываем изображение
cv2.imshow('Contours', image)

cv2.waitKey(0)
cv2.destroyAllWindows()