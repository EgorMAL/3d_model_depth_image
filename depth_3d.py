import numpy as np
import cv2

image = cv2.imread("./RealSense_Images/RealSense_Test_3.png")

# Преобразуем изображение в градации серого
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Устанавливаем нижнюю и верхнюю границы
lower_bound = 40  # Например, 50
upper_bound = 255 # Например, 150

# Создаем маску
mask = np.zeros_like(gray_image)  # Инициализируем маску нулями (черным цветом)
mask[(gray_image >= lower_bound) & (gray_image <= upper_bound)] = 255  # Устанавливаем белый цвет для пикселей внутри границ

cv2.imshow('Masked', mask)

# Находим контуры на изображении
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на оригинальном цветном изображении
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Показываем изображение
cv2.imshow('Contours', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
