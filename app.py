#Usage: python app.py
import os
 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
import numpy as np
import argparse
import imutils
import cv2
import time
import uuid
import base64

app = Flask(__name__)

@app.route("/")
def index():
    import tensorflow as tf
    return "A versão do tensorflow é"  + tf.__version__

if __name__ == "__main__":
    app.debug=true
    app.run(host='0.0.0.0', port=3000)
