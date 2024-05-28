import os
import streamlit as st
import shutil
from src.image_fct import *

def depotFichiers(data):
    if st.session_state["mode"]:
        # Upload des fichiers
        st.session_state["files"] = st.sidebar.file_uploader(label="Déposer les sources à visualiser", accept_multiple_files =True) #, on_change=batchChange, args=[data])
    else:
        path_dir = st.sidebar.text_input(label="Selection un répertoire", label_visibility="collapsed",  placeholder=r"[expl :] \\lilia\diskC\BASE")
        if os.path.isdir(path_dir):
            st.session_state["files"] = os.scandir(path_dir)
        else:
            st.session_state["files"] = None
            st.warning("Le path n'est pas valide")


def saveInput(tmpUpload):
    for file in st.session_state["files"]:
        with open(os.path.join(tmpUpload, file.name), "wb") as f:
            f.write(file.getbuffer())


def clear_mode(data):
    st.session_state["mode"] = 0
    clearData(data)
    st.session_state["upload"] = 0
    st.session_state['label_color'] = {}
    st.session_state["files"] = None

    
def clearData(path):
    for file in os.scandir(path):
        if os.path.isfile(file.path):
            os.remove(file.path)
        else:
            clearData(file.path)

def clearRegex():
    st.session_state["regex"] = False


def batchChange(data):
    st.session_state["upload"] = 0
    clearData(data)
    st.session_state['label_color'] = {}
    st.session_state["files"] = None
    st.session_state["rang_courant"] = 0

#@st.cache_data
def getImages2():
    listfilenames = []
    tempdict = {}
    for f in st.session_state["files"]:
        split_tup = os.path.splitext(f.path)
        if len(split_tup) == 2 and split_tup[1].lower() in ['.jpg', '.rot', '.tif']:
            nomsansext = split_tup[0]
            if nomsansext not in tempdict:
                tempdict[nomsansext] = []
            tempdict[nomsansext].append(split_tup[1].lower())
    for key in tempdict:
        if '.jpg' in tempdict[key]:
            listfilenames.append(key + '.jpg')
        elif '.rot' in tempdict[key]:
            listfilenames.append(key + '.rot')
        else:
            listfilenames.append(key + '.tif')

    return listfilenames


#@st.cache_data
def getImages(source):
    if os.path.exists(source) and os.path.isdir(source):
        listfilenames = []
        tempdict = {}
        for f in os.listdir(source):
            split_tup = os.path.splitext(f)
            if len(split_tup) == 2 and split_tup[1].lower() in ['.jpg', '.rot', '.tif']:
                nomsansext = source + '\\' + f.replace(split_tup[1], '')
                #nomsansext = f.replace(split_tup[1], '')
                if nomsansext not in tempdict:
                    tempdict[nomsansext] = []
                tempdict[nomsansext].append(split_tup[1].lower())
        for key in tempdict:
            if '.jpg' in tempdict[key]:
                listfilenames.append(key + '.jpg')
            elif '.rot' in tempdict[key]:
                listfilenames.append(key + '.rot')
            else:
                listfilenames.append(key + '.tif')
        return listfilenames
    else:
        return None

