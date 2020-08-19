
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify, abort
from dithering import dither
import uuid
import os

app = Flask(__name__)

# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/upload', methods=['POST'])
def route_upload():
    filename = str(uuid.uuid4())
    img = request.files['image']
    filename_orig = f'{filename}.{img.filename.split(".")[-1]}'
    filename_orig = os.path.join(uploads_dir, filename_orig)
    filename_tgt = f'{filename}'
    filename_tgt = os.path.join(uploads_dir, filename_tgt)
    img.save(os.path.join(uploads_dir, filename_orig))
    w = 0
    h = 0
    if 'width' in request.form:
        w = int(request.form['width'])
    if 'height' in request.form:
        h = int(request.form['height'])
    dither_res = dither(filename_orig, filename_tgt, w, h)
    if dither_res:
        print('alele')
        return jsonify(filename=filename)
    else:
        print('sukoshin')
        abort(404)