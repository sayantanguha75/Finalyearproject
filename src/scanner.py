from config import *
from loguru import logger
from utils import *
import time
from datetime import datetime

class ScanBarCode:
    def __init__(self, images_original, images, barcode_type="QRCODE"):
        self.images = images
        self.scanned_image = dict()
        self.images_original = images_original
        self.barcode_type=barcode_type
        self.barcode_dtls = dict()
        logger.warning("SCANNER OBJECT CREATED")

    def fit(self, mode="pyzbar"):
        for idx, image in self.images.items():
            logger.warning(f"SCANNING: {idx} Image")
            try:
                if not len(image):
                    logger.warning("Empty or Corrupted Image File Found and Skipping")
                    continue
            except Exception as ex:
                logger.error(f"Error Loading file: {ex}")
                continue
            # barcode = self._decode_image(image)
            # status = self._transform(barcode, image)
            start = time.time()
            status, barcode_dict = SCANNER_ENGINE[mode](self.images_original[idx], image, barcode_type=self.barcode_type)
            end = time.time()
            if status:
                logger.info(f"Successfully extracted barcode from: {idx} Image")
                self.scanned_image[idx] = self.images_original[idx]
                self.barcode_dtls[idx] = barcode_dict
                self.barcode_dtls[idx].update({
                    "Processing Details":{
                        "Start Time": str(datetime.fromtimestamp(start)),
                        "End Time": str(datetime.fromtimestamp(end)),
                        "Duration": str((end-start)*1000)+' Milliseconds'
                    }
                })
            else:
                logger.error(f"Failed to extract barcode from: {idx} Image")
        return self.scanned_image, self.barcode_dtls

