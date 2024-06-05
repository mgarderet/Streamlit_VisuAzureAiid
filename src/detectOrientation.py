import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import streamlit as st
import numpy as np
from PIL import Image
import cv2

def initMoteurDetectOrientation():
    """ Initialisation modèle IA detectOrientation """
    model_file_6conv3dense = os.path.join(st.session_state["moteursIA"], "cir2022-p32-orientation-et-rejet-6conv3dense.h5")
    st.session_state["modelIA"] = load_model(model_file_6conv3dense)


def pretraitementImageDetectOrientation():
    """Prétraitement image avant soumission au modèle IA detectOrientation"""
    image = Image.open(st.session_state["current_image_path"])
    image = image.resize((320, 320))
    image_array = np.array(image)

    #image = cv2.imread(st.session_state["current_image_path"], cv2.IMREAD_IGNORE_ORIENTATION)
    #image = cv2.resize(image, (320, 320), None, 0, 0, cv2.INTER_AREA)
    image_array = np.expand_dims(image_array, axis=0)  # Add an extra dimension for batch size
    image_array = image_array / 255.0  # Normalize the image data
    st.session_state["imagePRED"] = image_array


def predictDetectOrientation():
    """Prediction d'une image via modele IA detectOrientation"""
    st.session_state["predictModelDetectOrientation"] = st.session_state["modelIA"].predict(st.session_state["imagePRED"])


def resultDetectOrientation():
    """Récupération des résultats"""
    labels = [0, 1, 2, 3, "REJET"]
    predicted_class = np.argmax(st.session_state["predictModelDetectOrientation"][0])
    st.session_state['predictedLabel'] = labels[predicted_class]
    st.session_state['predictedScore'] = np.max(st.session_state["predictModelDetectOrientation"][0])