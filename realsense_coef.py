import pyrealsense2 as rs

# Создаем объект pipeline
pipeline = rs.pipeline()

# Настройка и старт pipeline
config = rs.config()
pipeline.start(config)

try:
    # Получаем профиль потока
    profiles = pipeline.get_active_profile()
    depth_profile = rs.video_stream_profile(profiles.get_stream(rs.stream.depth))
    color_profile = rs.video_stream_profile(profiles.get_stream(rs.stream.color))

    # Получаем внутренние параметры камеры для глубины и цвета
    depth_intrinsics = depth_profile.get_intrinsics()
    color_intrinsics = color_profile.get_intrinsics()

    # Выводим параметры
    print("Depth Intrinsics: ", depth_intrinsics.ppy)
    print("Color Intrinsics: ", color_intrinsics.coeffs)
finally:
    pipeline.stop()
