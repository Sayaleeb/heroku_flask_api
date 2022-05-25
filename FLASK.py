import os
import json
import base64
import requests
from detect_object import *
from PIL import Image
from io import BytesIO
from flask import Flask, jsonify, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save('static/images/'+ secure_filename(f.filename))
        
        # Make prediction
        
        get_detected_object=run_inference('static/images/'+f.filename)

        print(get_detected_object.shape)
        
        _, im_arr = cv2.imencode('.jpg', get_detected_object)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes).decode()        
  
        return {"image": im_b64}
        

if __name__ == '__main__':
    app.run(debug=True,port=4000)


     