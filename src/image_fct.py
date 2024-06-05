import os.path
from PIL import Image
import cv2
import streamlit as st
import numpy as np
from src.detectOrientation import *
import sys


def rotation():
    if st.session_state["rotate"] < 3:
        st.session_state["rotate"] += 1
    else :
        st.session_state["rotate"] = 0


def rotate_operateur():
    print(st.session_state["rotate"])
    if st.session_state["rotate"] == 1:
        st.session_state["imageROT"] = cv2.rotate(st.session_state["imageORI2"], cv2.ROTATE_90_CLOCKWISE)
    elif st.session_state["rotate"] == 2:
        st.session_state["imageROT"] = cv2.rotate(st.session_state["imageORI2"], cv2.ROTATE_180)
    elif st.session_state["rotate"] == 3:
        st.session_state["imageROT"] = cv2.rotate(st.session_state["imageORI2"], cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        st.session_state["imageROT"] = st.session_state["imageORI2"]


def detectOrientation_operateur():
    if st.session_state["ADO"] :
        try:
            initMoteurDetectOrientation()
            pretraitementImageDetectOrientation()
            predictDetectOrientation()
            resultDetectOrientation()
            if st.session_state['predictedScore'] >= st.session_state['seuilADO']:
                st.session_state["rotate"] = st.session_state['predictedLabel']
            else:
                st.session_state["rotate"] = 0
                st.session_state['predictedLabel'] = "?"

        except Exception as e:
            st.session_state["rotate"] = 0
    else:
        st.session_state['predictedLabel'] = None
        st.session_state["predictedScore"] = None
        st.session_state["rotate"] = 0


def gestion_outilsImage():
    detectOrientation_operateur()
    rotate_operateur()


def create_opencv_image_from_stringio(img_bytes, cv2_img_flag=0):
    img_array = np.asarray(bytearray(img_bytes), dtype=np.uint8)
    return cv2.imdecode(img_array, -1)


def createImageFromFile(path_image):
    #image = None
    if '.jpg' in path_image or '.tif' in path_image :
        st.session_state["imageORI"] = cv2.imread(path_image, cv2.IMREAD_UNCHANGED)
    elif '.rot' in path_image:
        with open(path_image, 'rb') as f:
            img_bytes = f.read()
        st.session_state["imageORI"] = create_opencv_image_from_stringio(img_bytes)


def generateImage(format_image):
    if st.session_state["current_image_path"]:
        path_name, ext = os.path.splitext(st.session_state["current_image_path"])
        if not ext == format_image:
            if os.path.isfile(path_name + format_image):
                st.session_state["current_image_path"] = path_name + format_image

        createImageFromFile(st.session_state["current_image_path"])

        if len(st.session_state["imageORI"].shape) == 2:
            st.session_state["imageORI2"] = cv2.cvtColor(st.session_state["imageORI"], cv2.COLOR_GRAY2RGB, cv2.IMREAD_UNCHANGED)

        else:
            st.session_state["imageORI2"] = st.session_state["imageORI"].copy()

