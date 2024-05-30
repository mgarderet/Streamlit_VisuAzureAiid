import os.path
from PIL import Image
import cv2
import streamlit as st
import numpy as np


def rotation():
    print("ici", st.session_state["rotate"])
    if st.session_state["rotate"] < 3:
        st.session_state["rotate"] += 1
    else :
        st.session_state["rotate"] = 0


def create_opencv_image_from_stringio(img_bytes, cv2_img_flag=0):
    img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)


def createImageFromFile(path_image):
    #image = None
    if '.jpg' in path_image or '.tif' in path_image :
        st.session_state["image"] = cv2.imread(path_image)
    elif '.rot' in path_image:
        with open(path_image, 'rb') as f:
            img_bytes = f.read()
        st.session_state["image"] = create_opencv_image_from_stringio(img_bytes)


def generateImage(path_image, format_image):
    path_name, ext = os.path.splitext(path_image)
    if not ext == format_image:
        if os.path.isfile(path_name + format_image):
            path_image = path_name + format_image

    createImageFromFile(path_image)

    if len(st.session_state["image"].shape) == 2:
        st.session_state["image"] = cv2.cvtColor(st.session_state["image"], cv2.COLOR_GRAY2RGB)

    else:
        st.session_state["image"] = st.session_state["image"].copy()

