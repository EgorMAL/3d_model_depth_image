"""Run this file to build 3-D model"""
from updated_model3d import Model3d
from consts import IMAGE_PATH, BOX_QUEUE

model = Model3d(images_path=IMAGE_PATH, box_queue=BOX_QUEUE)
model.run()
