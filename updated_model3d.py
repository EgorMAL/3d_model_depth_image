"""Model 3d"""
import os
import json
import matplotlib.pyplot as plt
from consts import IMAGE_PATH, BOX_QUEUE
from pallet import Pallet
from box import Box
from packer import Packer
from painter import draw_box

class Model3d():
    def __init__(self, imagesPath=IMAGE_PATH, boxQueue=BOX_QUEUE):
        self.imagePath = imagesPath
        self.boxQueue = boxQueue
        self.fig = plt.figure()
        self.axGlob = plt.axes(projection='3d')

    def get_boxes(self):
        boxes = {"boxes" : []}
        with open(BOX_QUEUE) as f:
            lines = f.readlines()
            for row in lines[1::]:
                row = row.split(',')
                box = {"id": int(row[0]), "x": float(row[1]), "y": float(row[2]), "z": float(row[3])}
                boxes["boxes"].append(box)
        self.boxes = boxes

    def get_images(self):
        dirname = IMAGE_PATH
        imagePathes = []
        imagesNumbers = []
        for file in os.listdir(dirname):
            filename = dirname + file
            imagePathes.append(filename)
            imagesNumbers.append(int(file.split('_')[0]))
        imagePathes = [x for y,x in sorted(zip(imagesNumbers, imagePathes))]
        self.image_pathes = imagePathes

    def find_pallet_bounding_box(self):
        self.pallet = Pallet(self.image_pathes[0])
        self.pallet.find_bounding_box()

    def create_packer(self):
        self.packer = Packer(self.pallet)

    def create_model(self):
        self.packed_boxes_info = []
        self.unpacked_cargos_info = []

        # FOR EDWARD
        self.top_boxes = []
        #

        i = 2
        iteration = 0
        for box in self.boxes["boxes"]:
            boxes_info = {}
            image_path = self.image_pathes[i - 1]
            i += 1
            box = Box(box_id=box["id"], x=box["x"], y=box["y"], z=box["z"], image_path=image_path)

            boxes_info["calculated_size"] = {
            "width": round(float(box.size[0]) * 0.01, 4),
            "length": round(float(box.size[1]) * 0.01, 4),
            "height": round(float(box.size[2]) * 0.01, 4)}
            boxes_info["cargo_id"] = box.id
            boxes_info["id"] = box.id
            boxes_info["mass"] = 1


            self.packer.append_box(box)
            box.get_bounding_box_coordinates(self.packer.queue[iteration], self.pallet)
            box.find_under_box_id(self.packer, i - 1)
            iteration += 1
            box.find_box_axes(self.pallet)
            box.find_box_sizes_in_3d()
            box.find_box_start_point_3d(pallet=self.pallet, queue=self.packer.queue[1::])
            boxes_info["position"] = {
                "x": round(float(box.start_point[2]) + round(float(box.d[2])) * 0.01 / 2, 4),
                "y": round(float(box.start_point[1]) + round(float(box.d[1])) * 0.01 / 2, 4),
                "z": round(float(box.start_point[0]) + round(float(box.d[0])) * 0.01 / 2, 4)}
            boxes_info["size"] = {
            "width": round(float(box.d[0]) * 0.01, 4),
            "height": round(float(box.d[1]) * 0.01, 4),
            "length": round(float(box.d[2]) * 0.01, 4)
            }
            boxes_info["sort"] = 1
            boxes_info["stacking"] = True
            boxes_info["turnover"] = True
            boxes_info["type"] = "box"
            self.packed_boxes_info.append(boxes_info)

            draw_box(box, self.axGlob)
        plt.show()

    def create_output_json(self):
        outputDict = {
        "cargoSpace": {
        "loading_size": {
        "length": 0 * 0.01,
        "height": self.pallet.y * 0.01,
        "width": self.pallet.x * 0.01
        },
        "position": [
        0 * 0.01 / 2,
        self.pallet.y * 0.01 / 2,
        self.pallet.x * 0.01 / 2
        ],
        "type": "pallet"
        },
        "cargos": self.packed_boxes_info,
        "unpacked": self.unpacked_cargos_info
        }

        with open("./Output/output.json", 'w') as fp:
            json.dump(outputDict, fp)

    def run(self):
        self.get_boxes()
        self.get_images()
        self.find_pallet_bounding_box()
        self.create_packer()
        self.create_model()
        self.create_output_json()
