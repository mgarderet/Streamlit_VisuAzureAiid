import os.path

import cv2
import streamlit as st
import numpy as np

def create_opencv_image_from_stringio(img_bytes, cv2_img_flag=0):
    img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)


#@st.cache_data
def createImageFromFile(path_image):
    image = None
    if '.jpg' in path_image or '.tif' in path_image :
        image = cv2.imread(path_image)
    elif '.rot' in path_image:
        with open(path_image, 'rb') as f:
            img_bytes = f.read()
        image = create_opencv_image_from_stringio(img_bytes)
    return image


#@st.cache_data
def generateImage(path_image, format_image):
    path_name, ext = os.path.splitext(path_image)
    if not ext == format_image:
        if os.path.isfile(path_name + format_image):
            path_image = path_name + format_image
    image = createImageFromFile(path_image)
    if len(image.shape) == 2:
        image_decoree = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    else:
        image_decoree = image.copy()

    return image_decoree
