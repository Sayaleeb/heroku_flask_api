import os
import glob
import json
import base64
import requests
import urllib.parse
from PIL import Image
from io import BytesIO
from detect_object import *
from gevent.pywsgi import WSGIServer
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, redirect, url_for, request, render_template



# Define a flask app
app = Flask(__name__)


img_folder = os.path.join('static','images')
app.config['UPLOAD_FOLDER'] = img_folder


@app.route("/")
def index():
  return render_template("index.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print("within slash")
    if request.method == 'POST':
        print('within POST request')
        f = request.files['file']
        f.save('static/images/'+ secure_filename(f.filename))
        
        url = 'http://127.0.0.1:4000/'

        # Make prediction
        files = {'file': open('static/images/'+f.filename, 'rb')}
        response = requests.post(url = url, files = files)
        print(response.status_code)
        #get_detected_object=run_inference('static/images/'+f.filename)
        #print(get_detected_object.shape)
        
        #_, im_arr = cv2.imencode('.jpg', req)  # im_arr: image in Numpy one-dim array format.
        #im_bytes = im_arr.tobytes()
        #im_b64 = base64.b64encode(im_bytes).decode()        
  
        #im_b64 = base64.b64encode(response.json()['image']).decode()
        im_b64=response.json()['image']

        return render_template("uploaded.html", display_detection = 'data:image/png;base64, '+im_b64)
        

if __name__ == '__main__':
    app.run(debug=True, port=1000)






