import re
from difflib import SequenceMatcher


dico_regex = {
    "Plaque_Fr":"[A-HJ-NP-TV-Z]{2}[\s-]{0,1}[0-9]{3}[\s-]{0,1}[A-HJ-NP-TV-Z]{2}|[0-9]{2,4}[\s-]{0,1}[A-Z]{1,3}[\s-]{0,1}[0-9]{2}",
    "Date_Numérique":"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}",
    "Permis_Fr":"[\s][0-9]{2}[0|1][0-9][0-9]{2}[0-9]{2}[0-9]{4}[\s]",
    "Montant":"[\s]?\d*?[\s]?\d*?[\s]\d*[.,]\d{2}[\s]",
    }


def traite_recherche(pattern, text, ratio=0.7):
    text = text.replace("\n", "  \n")
    if len(pattern) > 0:
        elements = re.findall(pattern, text)
        mots_proche = [mot for mot in text.split() if SequenceMatcher(None, pattern, mot).ratio() >= ratio]

        if len(elements) > 0:
            for element in elements:
                text = text.replace(element, " :red[{}] ".format(element))
                if element in mots_proche:
                    mots_proche.remove(element)
            return text, elements, mots_proche

        else:
            return text, [], mots_proche

    else:
        return text, [], []