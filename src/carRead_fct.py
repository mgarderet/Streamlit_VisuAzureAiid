import os
import unicodedata
import streamlit as st
#@st.cache_data
def TexteFromImage(select_image):
    pathCar = os.path.splitext(select_image)[0] + '.car'
    if os.path.isfile(pathCar):
        pathTxtCar = parseCAR(pathCar)
        if not os.path.isfile(pathTxtCar):
            return "Erreur dans la récupération des données."

        else:
            with open(pathTxtCar, encoding="utf-8") as f:
                read_data = f.read()
            return read_data


def parseCAR(src):
    data_car, upLoadCar_name = os.path.split(src)
    pathTxtCar = os.path.join(data_car, upLoadCar_name[:-4] + '.txt')

    try:
        if os.path.exists(src):
            fCAR = FichierCAR(src)
            fCAR.lireFichier()

            with open(pathTxtCar, "wb") as f:
                s = str(fCAR)
                u = s.encode('utf-8')
                f.write(u)

            return pathTxtCar

    except Exception as e:
        message = "parseCAR - Probleme (" + str(e) + ")\n"
        return message


######################################################
# Classe de gestion des caractères du fichier CAR
#######################################################
class CaractereFichierCAR:
    #######################################################
    # Constructeur de la classe
    #######################################################
    def __init__(self):
        self.score = 0
        self.ox = 0
        self.oy = 0
        self.fx = 0
        self.fy = 0
        self.reco = ''

    #######################################################
    # Transformation en texte
    #######################################################
    def __str__(self):
        return "%s (score = %d, ox = %d, ox = %d,ox = %d,ox = %d)" % (self.reco, self.score, self.ox, self.oy, self.fx,
                                                                      self.fy)


#######################################################
# Classe de gestion des mots du fichier CAR
#######################################################
class MotFichierCAR:
    #######################################################
    # Constructeur de la classe
    #######################################################
    def __init__(self):
        self.score = 0
        self.reco = ''
        self.ox = 100000
        self.oy = 100000
        self.fx = 0
        self.fy = 0
        self.cx = 0
        self.cy = 0
        self.caracteres = []

    #######################################################
    # Transformation en texte
    #######################################################
    def __str__(self):
        return "%s\t(score = %d, cx = %d, cy = %d, ox = %d, oy = %d, fx = %d, fy = %d)" % (
        self.reco, self.score, self.cx, self.cy, self.ox, self.oy, self.fx, self.fy)

    #######################################################
    # Ajout d'un caractere
    #######################################################
    def ajouterCaractere(self, c):
        nbCaracteres = len(self.caracteres)
        self.cx = int(((self.cx * nbCaracteres) + (c.fx + c.ox) / 2) / (nbCaracteres + 1))
        self.cy = int(((self.cy * nbCaracteres) + (c.fy + c.oy) / 2) / (nbCaracteres + 1))
        self.caracteres.append(c)
        if c.ox < self.ox:
            self.ox = c.ox
        if c.oy < self.oy:
            self.oy = c.oy
        if c.fx > self.fx:
            self.fx = c.fx
        if c.fy > self.fy:
            self.fy = c.fy
        self.score += c.score
        self.reco += c.reco

    #######################################################
    # Lecture du centre de la ligne en y
    #######################################################
    def centre(self, c):
        nbCaracteres = len(self.caracteres)
        sommex = 0
        for c in self.caracteres:
            sommex += c.fx - c.ox
        sommey = 0
        for c in self.caracteres:
            sommey += c.fy - c.oy
        return [int(sommex / nbCaracteres), int(sommey / nbCaracteres)]


#######################################################
# Classe de gestion des lignes du fichier CAR
#######################################################
class LigneFichierCAR:
    #######################################################
    # Contructeur de la classe
    #######################################################
    def __init__(self):
        self.mots = []
        self.position = 0

    #######################################################
    # Ajout d'un mot a la ligne
    #######################################################
    def ajouterMot(self, mot):
        nbMots = len(self.mots)
        self.position = int(((self.position * nbMots) + mot.cy) / (nbMots + 1))
        self.mots.append(mot)

    #######################################################
    # Transformation en texte
    #######################################################
    def __str__(self):
        # retour = "pos = %d\t:\t" % self.position
        retour = ""
        for mot in self.mots:
            retour += mot.reco + " "
        return retour


#######################################################
# Classe de gestion des fichier CAR ABBYY
#######################################################
class FichierCAR:
    #######################################################
    # Constructeur de la classe
    #######################################################
    def __init__(self, nomFichier):
        self.nomFichier = nomFichier
        self.mots = []
        self.lignes = []

    #######################################################
    # Transformation en texte
    #######################################################
    def __str__(self):
        # retour = "______________________________________________\n"
        # retour += "Fichier : " + self.nomFichier + "\n"
        # retour += "Mots : \n"
        # for mot in self.mots :
        #    retour += "\t%s\n" % str(mot)
        # retour += "\nLignes : \n"
        retour = ""
        for ligne in self.lignes:
            retour += "%s\n" % str(ligne)
        # retour += "______________________________________________\n"
        return retour

    #######################################################
    # Lance la lecture du fichier
    #######################################################
    def lireFichier(self):
        f = None
        mot = MotFichierCAR()
        try:
            f = open(self.nomFichier, "r")
            ligne = f.readline()
            while (ligne is not None) and (len(ligne) > 0):
                # Lecture d'un caractere
                if ligne[0] == '#':
                    # correction bug de ABBYY qui renvoie des lignes aberrantes
                    if (mot.ox >= 0 and
                            mot.oy >= 0 and
                            mot.ox < 100000 and
                            mot.oy < 100000 and
                            mot.fx >= mot.ox and
                            mot.fx < 100000 and
                            mot.fy >= mot.oy and
                            mot.fy < 100000):
                        self.mots.append(mot)
                        self.positionnerLigne(mot)
                    mot = MotFichierCAR()
                elif ligne[0] == '?\n':
                    # Fin de paragraphe
                    pass
                else:
                    elms = ligne.split('|')
                    if len(elms) == 6:
                        # Creation du caractere
                        c = CaractereFichierCAR()
                        c.score = float(float(elms[4]) / 55.00);
                        c.ox = int(elms[0][2:])
                        c.oy = int(elms[1])
                        c.fx = int(elms[2])
                        c.fy = int(elms[3])
                        # c.reco = filtre_character(ord(convert_character(ord(elms[5][:-1])).upper()))
                        c.reco = elms[5][:-1]
                        if c.reco != ' ':
                            mot.ajouterCaractere(c)
                        else:
                            self.mots.append(mot)
                            self.positionnerLigne(mot)
                            mot = MotFichierCAR()

                ligne = f.readline()
        finally:
            if f is not None:
                try:
                    f.close()
                except Exception as e:
                    raise Exception("Probleme de fermeture du fichier CAR pour lecture (" + str(e) + ")")

    #######################################################
    # Positionnement d'un mot dans une ligne
    #######################################################
    def positionnerLigne(self, mot):
        for ligne in self.lignes:
            if (ligne.position - 20) < mot.cy < (ligne.position + 20):
                ligne.ajouterMot(mot)
                return
        # Creation d'une nouvelle ligne
        ligne = LigneFichierCAR()
        ligne.ajouterMot(mot)
        self.lignes.append(ligne)


##########################################################
#
##########################################################

# def unaccent(str):
#     return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore')


##########################################################
#
##########################################################

