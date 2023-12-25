import pyrealsense2 as rs
import numpy as np
import cv2

# Настройка потоков данных
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
align_to_depth = rs.align(rs.stream.depth)
# Запуск потока
pipeline.start(config)

try:
    while True:
        # Получаем кадры
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Преобразование кадра в numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Преобразование в градации серого
        gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

        # Применяем размытие для уменьшения шума
        blurred = cv2.GaussianBlur(gray, (1, 1), 0)

        # dst = cv2.cornerHarris(blurred,2,3,0.04)
        # dst = cv2.dilate(dst,None)
        # color_image[dst>0.01*dst.max()]=[0,0,255]
        # Обнаружение границ с помощью Canny
        edged = cv2.Canny(blurred, 30, 150)

        # Находим контуры на изображении
        contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Рисуем контуры на оригинальном цветном изображении
        cv2.drawContours(color_image, contours, -1, (0, 255, 0), 2)

        # Показываем изображение
        cv2.imshow('Contours', color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Остановка потока
    pipeline.stop()
    cv2.destroyAllWindows()
