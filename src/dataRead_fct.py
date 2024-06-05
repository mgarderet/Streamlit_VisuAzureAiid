import os
from lxml import etree
import streamlit as st
import json


def DataFromImage() :
    """Retourne les données associées à une image

    Args:
        path_image: Chemin vers l'image dont on souhaite obtenir les données associées
        ext: Chaine de caractère intervenant dans la règle de nommage du fichier de donnée associé à l'image

    Returns:
        Un dictionnaire contenant les données associées à l'image
    """

    # Cas d'un fichier de donnée Azure AI ID (json)
    imgfile = os.path.splitext(st.session_state["current_image_path"])[0] + st.session_state["fdata_name"] + '.json'
    if os.path.isfile(imgfile):
        return traiteimgfile(imgfile)
    else:
        return {}


def traiteimgfile(file):

    dico = {'fulltext' : "", 'data' : {}, "metadata" : {}}

    try :
        with open(file, encoding="utf-8") as json_file:
            pydata = json.load(json_file)

            if 'content' in pydata.keys():
                # Récupération fulltext
                dico['fulltext'] = pydata['content']

            if 'api_version' in pydata.keys():
                dico['metadata']['api_version'] = pydata['api_version']

            if 'model_id' in pydata.keys():
                dico['metadata']['model_id'] = pydata['model_id']

            if 'documents' in pydata.keys():
                if 'doc_type' in pydata['documents'][0].keys():
                    dico['metadata']['doc_type'] = pydata['documents'][0]['doc_type']

                if 'fields' in pydata['documents'][0].keys():
                    for field in pydata['documents'][0]['fields']:
                        dico['data'][field] = pydata['documents'][0]['fields'][field]['content']

    finally:
        #print(dico)
        return dico


def postTraitement(dico):
    data = {}
    metadata = {}
    fulltext = None
    if len(dico.keys()) > 0:
        fulltext = dico['fulltext']
        data = dico['data']
        metadata = dico['metadata']

    return fulltext, data, metadata
