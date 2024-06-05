import os
import streamlit as st
import shutil
from src.image_fct import *


def saveInput():
    for file in st.session_state["upload"]:
        with open(os.path.join(st.session_state["path_tmp"], file.name), "wb") as f:
            f.write(file.getbuffer())


def clearHistory():
    if st.session_state["use_rang"] == 0:
        RecursiveDeleteFile(st.session_state["path_data"])
        st.session_state["use_rang"] += 1


def clear_mode(data):
    st.session_state["mode"] = 0
    RecursiveDeleteFile(data)
    st.session_state["upload"] = 0
    st.session_state['label_color'] = {}
    st.session_state["files"] = None
    st.session_state["Imagefiles"] = None
    st.session_state["current_image_path"] = None
    st.session_state["ADO"] = False

    
def RecursiveDeleteFile(path):
    for element in os.scandir(path):
        if os.path.isfile(element.path):
            os.remove(element.path)
        else:
            RecursiveDeleteFile(element.path)


def clearRegex():
    st.session_state["regex"] = False


def clearRotate():
    st.session_state["rotate"] = 0


def clearADO():
    st.session_state["ADO"] = False


def batchChange(data):
    st.session_state["upload"] = 0
    RecursiveDeleteFile(data)
    st.session_state['label_color'] = {}
    st.session_state["files"] = None
    st.session_state["rang_courant"] = 0


def getFilesList():
    """
    Permet la récupération intéractive des fichiers à traiter en fonction du mode sélectionné par l'utilisateur :
        * Mode 'fichier unitaire' --> IHM d'upload de fichier
        * Mode 'scrutation répertoire' --> Saisie d'un chemin vers un répertoire source valide

    :param: None
    :return: Liste des chemins vers les fichiers
    """
    if st.session_state["mode"]:
        # Upload des fichiers
        st.session_state["upload"] = st.sidebar.file_uploader(label="Déposer les sources à visualiser", accept_multiple_files =True, on_change=batchChange, args=[st.session_state["path_data"]])
        saveInput()
        st.session_state["files"] = os.scandir(st.session_state["path_tmp"])

    else:
        path_dir = st.sidebar.text_input(label="Selection un répertoire", label_visibility="collapsed",  placeholder=r"[expl :] \\lilia\diskC\BASE")
        if path_dir:
            if os.path.isdir(path_dir):
                st.session_state["files"] = os.scandir(path_dir)
            else:
                st.error("Le path n'est pas valide")
        else:
            st.warning("Veuillez indiquer un path")


def getImagesList():
    list_image = []
    list_ext = []
    tempdict = {}
    if st.session_state["files"]:
        for f in st.session_state["files"]:
            split_tup = os.path.splitext(f.path)
            if len(split_tup) == 2 and split_tup[1].lower() in ['.jpg', '.rot', '.tif']:
                if split_tup[1] not in list_ext :
                    list_ext.append(split_tup[1])
                nomsansext = split_tup[0]
                if nomsansext not in tempdict:
                    tempdict[nomsansext] = []
                tempdict[nomsansext].append(split_tup[1].lower())
        for key in tempdict:
            if '.jpg' in tempdict[key]:
                list_image.append(key + '.jpg')
            elif '.rot' in tempdict[key]:
                list_image.append(key + '.rot')
            else:
                list_image.append(key + '.tif')
    list_image.sort()
    if len(list_ext) == 1:
        list_ext.append(list_ext[0])
    st.session_state["Imagefiles"] = list_image
    st.session_state["Imageext"] = list_ext




