import pyrealsense2 as rs
import numpy as np
import cv2

# Настройка и запуск потока RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth)
config.enable_stream(rs.stream.color)
pipeline.start(config)

try:
    # Ждем, чтобы получить кадр
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    if not depth_frame or not color_frame:
        raise RuntimeError("Не удалось получить кадры")

    # Преобразование изображений в массивы NumPy
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # Получаем профиль потока
    profiles = pipeline.get_active_profile()
    depth_profile = rs.video_stream_profile(profiles.get_stream(rs.stream.depth))
    color_profile = rs.video_stream_profile(profiles.get_stream(rs.stream.color))

    # Получаем внутренние параметры камеры для глубины и цвета
    depth_intrinsics = depth_profile.get_intrinsics()
    color_intrinsics = color_profile.get_intrinsics()
    # Параметры калибровки камеры (примерные значения, замените на реальные)
    camera_matrix = np.array([[depth_intrinsics.fx, 0, depth_intrinsics.ppx],
                              [0, depth_intrinsics.fy, depth_intrinsics.ppy],
                              [0, 0, 1]], dtype=np.float32)
    dist_coeffs = np.array(depth_intrinsics.coeffs, dtype=np.float32)  # Предполагаем, что нет искажений

    # Коррекция искажений
    h, w = color_image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))
    color_image_undistorted = cv2.undistort(color_image, camera_matrix, dist_coeffs, None, new_camera_matrix)

    # Определение точек для преобразования перспективы
    # Так как камера в центре, точки можно определить как углы изображения
    pts_src = np.array([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]], dtype=np.float32)
    pts_dst = np.array([[0, 0], [640, 0], [0, 480], [640, 480]], dtype=np.float32)

    # Вычисление матрицы преобразования и применение ее
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    result = cv2.warpPerspective(color_image_undistorted, matrix, (640, 480))

    # Показать результат
    cv2.imshow('2D Top View', result)
    cv2.waitKey(0)
finally:
    pipeline.stop()

cv2.destroyAllWindows()
