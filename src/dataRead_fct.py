import os
from lxml import etree
import streamlit as st
import json


def TauxRecto():
    taux = 0

    return taux


def TauxVerso():
    taux = 0

    return taux


def DataFromImage(path_image, ext='_results') :
    """Retourne les données associées à une image

    Args:
        path_image: Chemin vers l'image dont on souhaite obtenir les données associées
        ext: Chaine de caractère intervenant dans la règle de nommage du fichier de donnée associé à l'image

    Returns:
        Un dictionnaire contenant les données associées à l'image
    """

    # Cas d'un fichier de donnée Azure AI ID (json)
    imgfile = os.path.splitext(path_image)[0] + ext + '.json'
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

                # categorie = object['name']
                #
                # if categorie in dico.keys():
                #     rang += 1
                #     dico2 = dico[categorie]
                #     dico2[categorie.lower() + '_' + str(rang)] = {}
                # else:
                #     dico2 = {}
                #     dico[categorie] = dico2
                #     dico2[categorie.lower() + '_' + str(rang)] = {}
                #
                # for data in object.keys():
                #     if data in valide_dataTag:
                #         dico[categorie][categorie.lower() + '_' + str(rang)][data] = object[data]
        #         if data.tag in valide_boxTag:
        #             liste_coord.append(data.text)
        #             dico[categorie.text][categorie.text.lower() + '_' + str(rang)]['rectangle'] = tuple(liste_coord)

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
