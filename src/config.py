from utils import *
import os

# This will goto Config
TRANSFORM_MAP = {
    "RGB_to_grey": convert_grey,
    "morph": morph,
    "sharpen": sharpen_image,
    "Binarize": binarize,
}

#THIS SHOULD GOTO CONFIG
SCANNER_ENGINE = {
    "pyzbar": transform_zbar,
    "opencv": transform_cv,
    

}

IMAGE_PATH = "../images"

IMG_DIR = {
    "raw": "../images/raw/original",
    "processed": "../images/processed",
    "transformed": "../images/transformed",
    "scanned": "../images/scanned",
}

if os.environ.get("ENV", "none") == "local":
    SYS_ROOT = "/Users/nishanali/WorkSpace/grow_bit"
elif os.environ.get("ENV", "none") == "server":
    SYS_ROOT = os.environ.get("SYS_ROOT", "path_to_the_server")
else:
    SYS_ROOT = os.environ.get("SYS_ROOT", "/app")

DATA_ROOT = os.path.join(SYS_ROOT,"data")
