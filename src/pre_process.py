import cv2
from loguru import logger
from config import *

class PreProcess:
    def __init__(self,images):
        self.images = images
        self.images_transformed = dict()
    
    def transform(self, modes=["RGB_to_grey"],display=False):
        c = 0
        for idx, image in self.images.items():

            try:
                if not len(image):
                    logger.warning("Empty or Corrupted Image File Found and Skipping")
                    continue
            except Exception as ex:
                logger.error(f"Error Loading file: {ex}, {idx}")
                continue
            c += 1
            logger.info(f"Begining Transformation for: {c} Image")
            try:
                mask = image.copy()
                for mode in modes:
                    mask = TRANSFORM_MAP[mode](mask)
                    logger.info(f"\t\tApplied: {mode} FILTER")
                # self.images_transformed.append(mask)
                self.images_transformed[idx] = mask

                if display:
                    logger.info(f"\t\tDisplaying Image: {c}")
                    plt.imshow(mask)

            except Exception as ex:
                logger.error(f"Failed to operate: {mode} for: {c} with Error: {ex}")
                continue
        logger.info("Transformation Completed...!!!!")
        return self.images_transformed

