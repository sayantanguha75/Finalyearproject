#app.py
import code
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from flask import Blueprint

bp = Blueprint('ingest',__name__,url_prefix='/growbit')

import os
from werkzeug.utils import secure_filename
from loguru import logger
from urllib.parse import urlparse, parse_qs
import sys
if os.environ.get("ENV","none")=="local":
    sys.path.append("/home/sayantan/Downloads/grow_bit-main/src")
else:
    sys.path.append("/app/src/")

from main import *


app = Flask(__name__)

 
UPLOAD_FOLDER = 'static/uploads'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
def format_data(data):
    code_map = dict()
    code_map["pa"] = "UPI_ADDRESS"
    code_map["tn"] = "Provider"
    code_map["pn"] = "Merchent"
    field = None
    flag = False
    if data.get("Primary Bar-Code"):
        dtls = data.get("Primary Bar-Code")
        flag=True
        field = "Primary Bar-Code"
        print("Primary Identified")
    elif data.get("Secondary Bar-Code"):
        dtls = data.get("Primary Bar-Code")
        flag=True
        field = "Secondary Bar-Code"
        print("Secondary Identified")
    else:
        print("NO TYPE IDENTIFIED")
    if flag and field:
        print("FLAG AND FIELD TRUE")
        print(f"DATA: {data.get(field)}")
        print(f"DATA TO BE PARSED: {data[field].get('BARCODE DATA', 'N/A')}")
        parsed = urlparse(data[field].get("BARCODE DATA", "N/A"))
        print(f"PARSED: {parsed}")
        query = parse_qs(parsed.query, keep_blank_values=True)
        print(f"QUERY: {query}")
        if query.get("tn"):
            data[field][code_map["pn"]] = query.get("pn")
            data[field][code_map["tn"]] = query.get("tn")
            data[field][code_map["pa"]] = query.get("pa")
        else:
            data[field][code_map["tn"]] = query.get("pn")
            data[field][code_map["pa"]] = query.get("pa")
            data[field][code_map["pn"]] = ["NOT PRESENT IN QR-DETAILS"]

    print(f"RETURNING DATA: {data}")
    return data

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    barcode_dtls = dict()

    barcode_type=selected = str(request.form.get("barcode_type"))
    logger.warning(f"Uploading Image: TYPE:{barcode_type}")
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        barcode_dtls = process_doc(file_path=os.path.join(app.config['UPLOAD_FOLDER']), save=False, ui=True, barcode_type=barcode_type)
        logger.warning(f"BARCODE DETAILS: {barcode_dtls}")
        data = format_data(barcode_dtls[filename])
        print(data)
        # return render_template('index.html', filename=filename, barcode_dtls=data)
        return data
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@bp.route('/extract_barcode_info', methods=["POST"])
def extract_barcode():
    barcode_dtls = dict()
    barcode_type= str(request.form.get("barcode_type", "QRCODE"))
    logger.warning(f"Uploading Image: TYPE:{barcode_type}")
    if 'file' not in request.files:
        return "NO FILE RECEIVED"
    
    file = request.files['file']

    if file.filename == '':
        flash('No image selected for uploading')
        return "CORRUPTED FILENAME...!!!"
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        folder_path = "../uploads"
        # folder_path = "/app/services/static/uploads"
        file.save(os.path.join(os.getcwd(), "services",app.config['UPLOAD_FOLDER'], filename)) 
        barcode_dtls = process_doc(file_path=os.path.join(os.getcwd(),"services",app.config['UPLOAD_FOLDER']), save=False, ui=True, barcode_type=barcode_type)
        logger.warning(f"BARCODE DETAILS: {barcode_dtls}")
        data = format_data(barcode_dtls[filename])
        if data:
            os.remove(os.path.join(os.getcwd(), "services",app.config['UPLOAD_FOLDER'], filename))
        return data
    else:
        return 'Allowed image types are - png, jpg, jpeg, gif'


@app.route('/display/<filename>')
def display_image(filename):
    logger.warning(f"Trying to display {filename}")
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()