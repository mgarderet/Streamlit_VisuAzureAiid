import os
import shutil
import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image

from src.generique_fct import *
from src.visualisation_IHM import *
from src.image_fct import *
from src.carRead_fct import *


st.set_page_config(
    page_title="Let's run!",
    page_icon="🏃‍",
    layout="wide",
)

st.markdown("# Description de l'outil ! 😀 #Mga0.0",
            help="# Documentation express"
                 "\n\nVous pouvez : "
                 "\n\n- charger des fichiers images (obligatoire) au fromat tif, jpg ou rot et des fichiers .json via la fenêtre d'upload"
                 "\n\n- désactiver le mode fichier unitaire pour indiquer un path vers un espace partagé contenant des fichiers images et .json"
                 "\n\n- naviguer entre les images via les boutons suivant / précédent ou selectionner directement une image dans la liste"
                 "\n\n- définir une règle de nommage spécifique pour les fichiers json (chaine insérée entre nom_image et .json)")

# Initialisation
if "rang_courant" not in st.session_state:
    st.session_state["rang_courant"] = 0
if "label_color" not in st.session_state:
    st.session_state["label_color"] = {}
if "use_rang" not in st.session_state:
    st.session_state["use_rang"] = 0
if "upload" not in st.session_state:
    st.session_state["upload"] = 0
if "mode" not in st.session_state:
    st.session_state["mode"] = 0
if "files" not in st.session_state:
    st.session_state["files"] = None
if "regex" not in st.session_state:
    st.session_state["regex"] = False

st.session_state["path_data"] = os.path.join(os.path.dirname(__file__), "data")
st.session_state["path_tmp"] = os.path.join(st.session_state["path_data"], 'tmpUpload')

if not os.path.isdir(os.path.join(os.path.dirname(__file__), "data")):
    os.mkdir(st.session_state["path_data"])
    os.mkdir(st.session_state["path_tmp"])

# Creation du layout des IHM
path_frame = st.container(border=True)
main_frame = st.container()
image_frame, text_frame = main_frame.columns(2)

with main_frame :

    # Initialisation des data
    if st.session_state["use_rang"] == 0:
        clearData(st.session_state["path_data"])
        st.session_state["use_rang"] += 1

    # Selection du mode de chargement des données (UpLoad (True) vs Path_dir (False))
    mode = st.sidebar.toggle(label='Mode fichier unitaire', value=True, on_change=clear_mode, args=[st.session_state["path_data"]])

    # Stockage dans la session du choix du mode
    if st.session_state["mode"] == 0:
        st.session_state["mode"] = mode

    # Récupération de la liste des fichiers (selon le mode selectioné)
    if st.session_state["mode"]:
        # Upload des fichiers
        st.session_state["files"] = st.sidebar.file_uploader(label="Déposer les sources à visualiser", accept_multiple_files =True, on_change=batchChange, args=[st.session_state["path_data"]])
    else:
        path_dir = st.sidebar.text_input(label="Selection un répertoire", label_visibility="collapsed",  placeholder=r"[expl :] \\lilia\diskC\BASE")
        if os.path.isdir(path_dir):
            st.session_state["files"] = os.scandir(path_dir)
        else:
            st.session_state["files"] = None
            st.warning("Le path n'est pas valide")

    if st.session_state["files"]:

        # Sauvegarde en local des fichiers si mode upload
        if st.session_state["mode"]:
            saveInput(st.session_state["path_tmp"])

            # Récupération des formats images (jpg, rot, tif)
            liste_image = getImages(st.session_state["path_tmp"])

        else:
            liste_image = getImages2()

        # Initialisation de la navigation
        if liste_image:
            if len(liste_image) > 1 :
                max_rang = len(liste_image)-1
            else :
                max_rang = len(liste_image)

            # Création des IHM de visualisation et navigation
            container_navigation, bouton_suivant, bouton_precedent = create_container_navigation(st.sidebar)

            # Gestion de la navigation
            if bouton_suivant :
                if st.session_state.rang_courant != max_rang:
                    st.session_state["rang_courant"] += 1
                clearRegex()

            if bouton_precedent :
                if st.session_state.rang_courant != 0 :
                    st.session_state["rang_courant"] -= 1
                clearRegex()

            # Selection de l'image courante (avec gestion du cas particulier d'une image)
            if len(liste_image) > 1 :
                select_image = st.sidebar.selectbox("Sélectionner une image", liste_image, index=st.session_state.rang_courant, on_change=clearRegex)
            else :
                select_image = st.sidebar.selectbox("Sélectionner une image", liste_image, index=0, on_change=clearRegex)


            # génération de l'image correspondant à toutes nos sélections
            image = generateImage(select_image)

            # Transformation en image PIL
            pilimage = Image.fromarray(image)

            # Affichage du path de l'image
            path_frame.text(select_image)

            # Afficher image avec fonction Zoom intégrée
            with image_frame:
                image_zoom(image, size=1000, mode="both", zoom_factor=8.0, increment=0.5)


            # Affichage des données associées à l'image courante
            expand_texte = text_frame.container(border=True)
            expand_texte.text("Retour de la fonction de prétraitement des données")


