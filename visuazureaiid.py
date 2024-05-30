import os
import shutil
import streamlit as st

from PIL import Image

from src.dataRead_fct import *
from src.generique_fct import *
from src.visualisation_IHM import *
from src.image_fct import *
from src.carRead_fct import *
from streamlit_image_zoom import image_zoom

st.set_page_config(
    page_title="Let's run!",
    page_icon="🏃‍",
    layout="wide",
)

st.markdown("# Visualiser les résultats Azure AI (Intelligence documentaire) ! 😀 #Mga 0.5",
            help="# Documentation express"
                 "\n\nVous pouvez : "
                 "\n\n- charger des fichiers images (obligatoire) au fromat tif, jpg ou rot et des fichiers .json via la fenêtre d'upload"
                 "\n\n- désactiver le mode fichier unitaire pour indiquer un path vers un espace partagé contenant des fichiers images et .json"
                 "\n\n- naviguer entre les images via les boutons suivant / précédent ou selectionner directement une image dans la liste"
            )

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
if "image" not in st.session_state:
    st.session_state["image"] = None
if "rotate" not in st.session_state:
    st.session_state["rotate"] = 0

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
                clearRotate()

            if bouton_precedent :
                if st.session_state.rang_courant != 0 :
                    st.session_state["rang_courant"] -= 1
                clearRegex()
                clearRotate()

            # Selection de l'image courante (avec gestion du cas particulier d'une image)
            if len(liste_image) > 1 :
                select_image = st.sidebar.selectbox("Sélectionner une image", liste_image, index=st.session_state.rang_courant, on_change=clearRegex)
            else :
                select_image = st.sidebar.selectbox("Sélectionner une image", liste_image, index=0, on_change=clearRegex)

            # Selection de la règle de nommage json
            ext = '_result'
            if st.sidebar.toggle('Nommage JSON spécifique',
                                 help=f"Chaine de caractère fixe qui sera insérée entre le nom de l'image et l'extension .json"
                                      f' Défaut : {ext}'):
                ext = st.sidebar.text_input('Nommage spécifique', value='', label_visibility="collapsed")
            st.sidebar.caption(f'_NOM_IMAGE{ext}.json_')

            # choix du format de l'image
            format_image = st.sidebar.select_slider(label='Format image', options=['.jpg', '.tif', '.rot'], help='[JPG, TIF, ROT]')

            # Champs API AZURE IdDocument
            liste_retour = ['DocumentNumber', 'DocumentDiscriminator', 'FirstName', 'LastName', 'Address', 'DateOfBirth', 'PlaceOfBirth', 'DateOfExpiration', 'DateOfIssue', 'Height', 'Sex']
            liste_recto = ['DocumentNumber', 'DocumentDiscriminator', 'FirstName', 'LastName', 'DateOfBirth', 'PlaceOfBirth', 'DateOfExpiration', 'Sex']
            liste_verso = ['Address', 'DateOfIssue', 'Height', 'DateOfExpiration']
            st.sidebar.dataframe(liste_retour, column_config={'value' : 'Spec. API Azure'})
            st.sidebar.dataframe(liste_recto, column_config={'value' : 'Spec. CNI recto'})
            st.sidebar.dataframe(liste_verso, column_config={'value' : 'Spec. CNI verso'})

            # génération de l'image correspondant à toutes nos sélections
            generateImage(select_image, format_image)

            # Transformation en image PIL
            #st.session_state["image"] = Image.fromarray(st.session_state["image"])

            # Affichage du path de l'image
            path_frame.text(select_image)
            print("la", st.session_state["rotate"])

            # Afficher image sans fonction Zoom intégrée
            with image_frame:
                barre_outils = image_frame.container()
                frame_image = image_frame.container()

                barre_outils.button(':arrows_counterclockwise:', on_click=rotation)


                if st.session_state["rotate"] == 1:
                    st.session_state["image"] = cv2.rotate(st.session_state["image"], cv2.ROTATE_90_CLOCKWISE)
                if st.session_state["rotate"] == 2:
                    st.session_state["image"] = cv2.rotate(st.session_state["image"], cv2.ROTATE_180)
                if st.session_state["rotate"] == 3:
                    st.session_state["image"] = cv2.rotate(st.session_state["image"], cv2.ROTATE_90_COUNTERCLOCKWISE)
                    # st.session_state["image"] = image
                    # st.session_state["rotate"] -= 1
                print("re", st.session_state["rotate"])

                #frame_image.image(st.session_state["image"])
                with frame_image:
                    image_zoom(st.session_state["image"], size=700, mode="both", keep_resolution=True, zoom_factor=8.0, increment=0.5)

            # Création de l'IHM d'affichage des données associées à l'image courante
            container_meta_data = text_frame.container(border=True)
            container_data = text_frame.container(border=True)
            expand_texte_fulltexte = text_frame.expander(label='Fulltext')
            container_perf = text_frame.container(border=True)
            col1, col2, col3 = container_perf.columns(3)

            # Recuperation des données de l'image
            dico_res = DataFromImage(select_image, ext)
            fulltext, data, metadata = postTraitement(dico_res)

            # Calcul des performances
            tx = max(len([data for data in data.keys() if data in liste_recto])/len(liste_recto), len([data for data in data.keys() if data in liste_verso])/len(liste_verso))
            nb_data = len(data.keys())

            # Affichage des méta données de l'image
            container_meta_data.write("Meta-data")
            container_meta_data.write(metadata)

            # Affichage des données de l'image
            container_data.write("Data")
            container_data.write(data)

            # Affichage du fulltext de l'image
            expand_texte_fulltexte.text(fulltext)

            # Affichage des indicateurs de performance
            col1.metric("Tx lect", f"{tx:.0%}")
            col2.metric("Nb data", nb_data)

