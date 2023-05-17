import cv2
import pyzbar.pyzbar as pyzbar
from pyzbar.pyzbar import ZBarSymbol
# import imutils
from kraken import binarization
from PIL import Image
import numpy as np
import os
import datetime
from loguru import logger


#This will goto Util
def convert_grey(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def morph(image):
    MASK_DILATE_ITER = 1
    MASK_ERODE_ITER = 1
    mask = cv2.dilate(image, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    return mask

def sharpen_image(image):
    image_blurred = cv2.GaussianBlur(image, (5, 5), 1)
    image_sharp = cv2.addWeighted(image, 1.5, image_blurred, -0.1, 0)
    return image_sharp

def binarize(image):
    return np.asarray(binarization.nlbin(Image.fromarray(image)))

# THIS SHOULD GOTO UTILS
def transform_zbar(image_original, image_processed,barcode_type):
    barcodes = pyzbar.decode(image_processed)
    tr_flag = False
    barcode_dtls = dict()
    try:
        for idx, barcode in enumerate(barcodes):
            decoded_value = barcode.data.decode('utf-8')
            
            if str(barcode.type)==barcode_type:
                logger.info(f"No: {idx+1}, Type: {barcode.type}, Data: {decoded_value}")
                points = np.array([barcode.polygon], np.int32)
                points = points.reshape(-1,1,2)
                cv2.polylines(image_original, [points], True, (255,0,0), 10)
                x,y = barcode.polygon[0]
                logger.warning(f"X: {x} Y: {y}")
                logger.warning(f"CO-Ordinates: {barcode.polygon[0]}")
                cv2.putText(image_original, f"{decoded_value}", (x+10,y-60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255,0,0), 2)        
                tr_flag = True
                if not barcode_dtls.get("Primary Bar-Code"):
                    barcode_dtls["Primary Bar-Code"] = {}    
                barcode_dtls["Primary Bar-Code"].update({"BARCODE DATA": str(decoded_value), "BARCODE TYPE": str(barcode.type)})
            else:
                logger.info(f"No: {idx+1}, Type: {barcode.type}, Data: {decoded_value}")
                points = np.array([barcode.polygon], np.int32)
                points = points.reshape(-1,1,2)
                cv2.polylines(image_original, [points], True, (255,0,0), 10)
                x,y = barcode.polygon[0]
                logger.warning(f"X: {x} Y: {y}")
                logger.warning(f"CO-Ordinates: {barcode.polygon[0]}")
                cv2.putText(image_original, f"{decoded_value}", (x+10,y-60), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255,0,0), 2)        
                
                if not barcode_dtls.get("Secondary Bar-Code"):
                    barcode_dtls["Secondary Bar-Code"] = {}
                barcode_dtls["Secondary Bar-Code"].update({"BARCODE DATA": str(decoded_value), "BARCODE TYPE": str(barcode.type)})
                logger.warning(f"BARCODE TYPE: {barcode.type} DID NOT MATCH WITH SPECIFIED TYPE:{barcode_type}")
                tr_flag = True
    except Exception as ex:
        logger.error(f"Error: {ex} occurred while transforming barcode info for {idx} image")
        return tr_flag, barcode_dtls
    return tr_flag, barcode_dtls

def transform_cv(image_original, image_processed): 
    import cv2
    bardet = cv2.legacy_barcode_BarcodeDetector()
    img = image_processed
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)

def save_results(images, img_dir, ui=False):
    if not ui:
        date_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        os.makedirs(os.path.join(img_dir,date_time), exist_ok = True)
        for idx, image in images.items():
            cv2.imwrite(os.path.join(os.path.join(img_dir,date_time),str(idx)+'.jpg'), image)
    else:
        for idx, image in images.items():
            image = cv2.resize(image, (640,640))
            cv2.imwrite(os.path.join(img_dir,str(idx)), image)