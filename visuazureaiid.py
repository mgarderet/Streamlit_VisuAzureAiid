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

st.markdown("# Visualiser les résultats Azure AI (Intelligence documentaire) ! 😀 #Mga 0.6",
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
    st.session_state["mode"] = False
if "ADO" not in st.session_state:
    st.session_state["ADO"] = False
if "files" not in st.session_state:
    st.session_state["files"] = None
if "fdata_name" not in st.session_state:
    st.session_state["fdata_name"] = None
if "Imagefiles" not in st.session_state:
    st.session_state["Imagefiles"] = []
if "Imageext" not in st.session_state:
    st.session_state["Imageext"] = []
if "regex" not in st.session_state:
    st.session_state["regex"] = False
if "imageORI" not in st.session_state:
    st.session_state["imageORI"] = None
if "imageORI2" not in st.session_state:
    st.session_state["imageORI2"] = None
if "imagePRED" not in st.session_state:
    st.session_state["imagePRED"] = None
if "imageROT" not in st.session_state:
    st.session_state["imageROT"] = None
if "current_image_path" not in st.session_state:
    st.session_state["current_image_path"] = None
if "rotate" not in st.session_state:
    st.session_state["rotate"] = 0
if "modelIA" not in st.session_state:
    st.session_state["modelIA"] = None
if "predictModelDetectOrientation" not in st.session_state:
    st.session_state["predictModelDetectOrientation"] = None
if "predictedLabel" not in st.session_state:
    st.session_state["predictedLabel"] = None
if "predictedScore" not in st.session_state:
    st.session_state["predictedScore"] = None


st.session_state["path_data"] = os.path.join(os.path.dirname(__file__), "data")
st.session_state["moteursIA"] = os.path.join(os.path.dirname(__file__), "moteursIA")
st.session_state["path_tmp"] = os.path.join(st.session_state["path_data"], 'tmpUpload')
st.session_state['seuilADO'] = 0.80

if not os.path.isdir(os.path.join(os.path.dirname(__file__), "data")):
    os.mkdir(st.session_state["path_data"])
    os.mkdir(st.session_state["path_tmp"])

# Creation du layout des IHM
path_frame = st.container(border=True)
main_frame = st.container()
image_frame, text_frame = main_frame.columns(2)
barre_outils_image = image_frame.container()
outil_1, outil_2, outil_3, outil_4 = barre_outils_image.columns(4)
panel_image = image_frame.container()

with (main_frame) :

    # Suppression de l'historique si nouvelle session
    clearHistory()

    # Selection du mode de chargement des données (UpLoad (True) vs Path_dir (False))
    st.session_state["mode"] = st.sidebar.toggle(label='Mode fichier unitaire', value=False, on_change=clear_mode, args=[st.session_state["path_data"]])

    # Récupération de la liste des fichiers (selon le mode selectioné)
    getFilesList()

    # Récupération de la liste des images depuis la liste des fichiers
    getImagesList()

    # Gestion de la navigation dans la liste des images
    gestion_navigation()

    if st.session_state["current_image_path"]:

        # Gestion de la règle de nommage des fichiers de données (json)
        gestion_nommage_fdata()

        # Choix du format de l'image à afficher
        ## TO DO: Doit être dynamique selon les formats d'image disponible pour la current selection
        format_image = st.sidebar.select_slider(label='Format image', options=st.session_state["Imageext"], help='[JPG, TIF, ROT]')


        # Affichage du path de l'image
        ## TO DO : Doit être dynamique en fonction du format d'image selectionné
        path_frame.text(st.session_state["current_image_path"])

        # Génération de l'image correspondant à toutes nos sélections
        generateImage(format_image)



        # Gestion de la zone image
        with image_frame:

            # Création des outils de la barre d'outils
            outil_1.button(':arrows_counterclockwise:', on_click=rotation)
            st.session_state["ADO"] = outil_3.toggle(label='ADO', help=f"Activer la détection orientation auto. "
                                                                       f"Seuil de {st.session_state['seuilADO']}. 1=90_CW | 2=180 | 3=90_CC")


            # Gestion des actions des outils
            gestion_outilsImage()

            # Affichage des retours de la detection d'orientation auto
            if st.session_state["ADO"]:
                outil_4.text({st.session_state['predictedLabel']:st.session_state["predictedScore"]})

            # Affichage de l'image avec fct zoom
            with panel_image:
                st.image(st.session_state["imageROT"])
                #image_zoom(st.session_state["imageROT"], size=700, mode="both", keep_resolution=True, zoom_factor=8.0, increment=0.5)


        # Champs API AZURE IdDocument
        liste_retour = ['DocumentNumber', 'DocumentDiscriminator', 'FirstName', 'LastName', 'Address', 'DateOfBirth', 'PlaceOfBirth', 'DateOfExpiration', 'DateOfIssue', 'Height', 'Sex']
        liste_recto = ['DocumentNumber', 'DocumentDiscriminator', 'FirstName', 'LastName', 'DateOfBirth', 'PlaceOfBirth', 'DateOfExpiration', 'Sex']
        liste_verso = ['Address', 'DateOfIssue', 'Height', 'DateOfExpiration']
        with st.sidebar.expander(label="Specifications"):
            st.dataframe(liste_retour, column_config={'value' : 'Spec. API Azure'})
            st.dataframe(liste_recto, column_config={'value' : 'Spec. CNI recto'})
            st.dataframe(liste_verso, column_config={'value' : 'Spec. CNI verso'})

        # Création de l'IHM d'affichage des données associées à l'image courante
        container_meta_data = text_frame.container(border=True)
        container_data = text_frame.container(border=True)
        expand_texte_fulltexte = text_frame.expander(label='Fulltext')
        container_perf = text_frame.container(border=True)
        col1, col2, col3 = container_perf.columns(3)

        # Recuperation des données de l'image
        dico_res = DataFromImage()
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

