import numpy as np
import cv2

image1 = cv2.imread("./RealSense_Images/RealSense_Color_4.png")
image2 = cv2.imread("./RealSense_Images/RealSense_Color_5.png")

gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
# Преобразуем изображение в градации серого
gray_image = gray_image2 - gray_image1
print(np.unique(gray_image))
# Устанавливаем нижнюю и верхнюю границы
lower_bound = 60  # Например, 50
upper_bound = 80 # Например, 150

# Создаем маску
mask = np.zeros_like(gray_image)  # Инициализируем маску нулями (черным цветом)
mask[(gray_image >= lower_bound) & (gray_image <= upper_bound)] = 255  # Устанавливаем белый цвет для пикселей внутри границ

cv2.imshow('Masked', mask)

# Находим контуры на изображении
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Рисуем контуры на оригинальном цветном изображении
cv2.drawContours(image2, contours, -1, (0, 255, 0), 2)

# Показываем изображение
cv2.imshow('Contours', image2)

cv2.waitKey(0)
cv2.destroyAllWindows()
