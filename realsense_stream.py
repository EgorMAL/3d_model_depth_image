import pyrealsense2 as rs
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()

# Configure the pipeline to stream depth frames
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
align_to_depth = rs.align(rs.stream.depth)

# Start streaming
pipeline.start(config)

# Wait for a coherent pair of frames: depth and color
frames = pipeline.wait_for_frames()
depth_frame = frames.get_depth_frame()

# Get the intrinsic parameters of the camera
intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

# Get the depth scale of the camera
depth_sensor = pipeline.get_active_profile().get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

for i in range(1, 11):
    try:
        k = 1
        depth_stack = np.random.rand(640, 480)
        while k <= 25:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()

            # Convert the depth frame to a numpy array
            depth_image = np.asanyarray(depth_frame.get_data())
            if k > 1:
                depth_stack = np.dstack((depth_stack, np.expand_dims(depth_image, axis=-1)))
            else:
                depth_stack = depth_image.copy()
            k += 1
        depth_median = np.median(depth_stack, axis=2)
        # Calculate distance in meters for each pixel
        distances = depth_median * depth_scale

        # Define the parallel plane depth (adjust this value based on your requirements)
        parallel_plane_depth = 1.4  # in meters

        # Calculate the distance from each pixel to the parallel plane
        distances_to_parallel_plane = np.abs(distances - parallel_plane_depth)

        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        output_color_path = f"RealSense_Images/RealSense_Color_{i}.png"
        output_depth_path = f"RealSense_Images/RealSense_Depth_{i}.png"
        cv2.imwrite(output_color_path, color_image)
        cv2.imwrite(output_depth_path, distances_to_parallel_plane * 255)  # Умножаем на 255 для правильного отображения

        # Display the image with distances to the parallel plane
        cv2.imshow("Distances to Parallel Plane", distances_to_parallel_plane)
        cv2.waitKey(0)
    except:
        print("Это было не просто смело, это было п*здец как смело!")
#  Stop streaming
pipeline.stop()
cv2.destroyAllWindows()