import os
import streamlit as st
from src.catalogue_regex import *
from src.generique_fct import *
from PIL import Image
#import cv2


def create_container_image(container_perspective) :
    container_image = container_perspective.container()
    return container_image


def create_bouton_navigation(container_navigation):
    col1, col2 = container_navigation.columns(2)
    return col1, col2


def create_container_navigation(container_perspective) :
    container_navigation = container_perspective.container()
    col1, col2 = create_bouton_navigation(container_navigation)
    bouton_precedent = col1.button("Precedent")
    bouton_suivant = col2.button("Suivant")
    return container_navigation, bouton_suivant, bouton_precedent    


def gestion_navigation():
    if st.session_state["Imagefiles"]:
        if len(st.session_state["Imagefiles"]) > 1 :
            max_rang = len(st.session_state["Imagefiles"])-1
        else :
            max_rang = len(st.session_state["Imagefiles"])

        # Création des IHM de visualisation et navigation
        container_navigation, bouton_suivant, bouton_precedent = create_container_navigation(st.sidebar)

        # Gestion de la navigation
        if bouton_suivant :
            if st.session_state["rang_courant"] != max_rang:
                st.session_state["rang_courant"] += 1
            clearRegex()
            clearRotate()

        if bouton_precedent :
            if st.session_state["rang_courant"] != 0 :
                st.session_state["rang_courant"] -= 1
            clearRegex()
            clearRotate()

        # Selection de l'image courante (avec gestion du cas particulier d'une image)
        if len(st.session_state["Imagefiles"]) > 1 :
            st.session_state["current_image_path"] = st.sidebar.selectbox("Sélectionner une image", st.session_state["Imagefiles"], index=st.session_state["rang_courant"], on_change=clearRegex, format_func=lambda x: x.split("\\")[-1])
        else :
            st.session_state["current_image_path"] = st.sidebar.selectbox("Sélectionner une image", st.session_state["Imagefiles"], index=0, on_change=clearRegex, format_func=lambda x: x.split("\\")[-1])


def create_container_visualisation(visualisation_frame) :
    container_perspective = visualisation_frame.container()
    container_image = container_perspective.container()
    vue_image, vue_index  = container_image.columns([1, 1])
    return container_perspective, vue_image, vue_index


def create_select_path_lot(container_selection) :
    select_path_lot = container_selection.text_input("Path vers les lots : ", value=r"\\vmlbpkyctest\Lots\SDR_RIB\SDR_RIB", placeholder="Indiquer le path vers le répertoire des lots")
    return select_path_lot


def create_select_version(container_selection):
    select_version = container_selection.selectbox("Choix de la version", liste_version)
    return select_version


def show_image(path_image, vue_image) :
    vue_image.image(Image.open(path_image), use_column_width='auto')


def show_index(liste_index, vue_index, rang) :
    for index in liste_index :
        vue_index.text_input(index, value=liste_index.at[rang,index])


def show_compar_index(compar, colfi2, nom_image) :
    index = cherche_compar(st.session_state.data_base, compar, nom_image)
    compar_index = colfi2.text_input("lad", value=index, key=0)


def gestion_nommage_fdata():
    st.session_state["fdata_name"] = '_result'
    if st.sidebar.toggle('Nommage JSON spécifique',
                         help=f"Chaine de caractère fixe qui sera insérée entre le nom de l'image et l'extension .json"
                              f' Défaut : {st.session_state["fdata_name"]}'):
        st.session_state["fdata_name"] = st.sidebar.text_input('Nommage spécifique', value='', label_visibility="collapsed")
    st.sidebar.caption(f'_NOM_IMAGE{st.session_state["fdata_name"]}.json_')


def create_sidebar_regex(str_texte, text_frame):
    with st.sidebar :
        st.session_state["regex"] = st.checkbox("Utiliser la recherche Regex", value=st.session_state["regex"])
        if st.session_state["regex"] :
            text_2 = ""
            active_catalogue = st.checkbox("Utiliser le catalogue Regex", value=True)
            if active_catalogue :
                pattern_std = st.radio("Catalogue Regex", dico_regex.keys())
            else :
                pattern = st.text_input("Regex")
                ratio = st.slider("Distance", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

            with st.form("Recherche") :

                submitted = st.form_submit_button('Submit')

                if submitted and st.session_state["regex"]:
                    regex_expander = text_frame.expander("Correspondance RegEx", expanded=True)
                    text_panel_regex = regex_expander.container()

                    if active_catalogue is False and len(pattern) > 0 :
                        text_2, match, mots_proche = traite_recherche(pattern, str_texte, ratio)
                    elif active_catalogue :
                        text_2, match, mots_proche = traite_recherche(dico_regex[pattern_std], str_texte)
                    else:
                        match, mots_proche = [], []

                    st.write("{} occurence(s)".format(len(match)))
                    st.write(match)
                    st.write("{} mot(s) proche(s)".format(len(mots_proche)))
                    st.write(mots_proche)

                    text_panel_regex.markdown(text_2)

