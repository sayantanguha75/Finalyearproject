import os
import cv2
from loguru import logger

class LoadData:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image_dict = dict()

    def process(self):
        for idx, img in enumerate(os.listdir(self.file_path)):
            # if idx==10:
            #     break
            # self.images.append(cv2.imread(os.path.join(self.file_path,img), cv2.IMREAD_UNCHANGED))
            self.image_dict[img] = cv2.imread(os.path.join(self.file_path,img), cv2.IMREAD_UNCHANGED)
        logger.warning(f"Loaded: {len(self.image_dict)} images from source")
        return self.image_dict

