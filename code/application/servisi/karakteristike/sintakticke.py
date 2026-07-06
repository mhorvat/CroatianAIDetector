import nltk
import numpy as np



# Varijable
hrv_veznici = ['i', 'pa', 'te', 'ni', 'niti', 'ili', 'samo', 'jedino', 'tek',
               'dakle', 'zato', 'stoga', 'a', 'ali', 'nego', 'no', 'već',
               'da', 'kako', 'neka', 'gdje', 'kamo', 'kuda', 'otkud', 'odakle', 
               'dokud', 'dokle', 'kad', 'otkad', 'otkako', 'dokad', 'pošto', 'dok', 
               'čim', 'jer', 'što', 'ako', 'li', 'koliko', 'iako', 'makar', 'premda']



# SINTAKTIČKE

# Prosječan broj riječi u rečenici
def prosjecanBrojTokenaURecenici(tekst):
        return tekst.broj_tokena() / tekst.broj_recenica()

def prosjecanBrojRijeciURecenici(tekst):
    return tekst.broj_rijeci() / tekst.broj_recenica()


# Standardna devijacija duljine rečenica
def standardnaDevBrojaTokenaURecenici(tekst):
    brojevi_tokena = [len(nltk.word_tokenize(r)) for r in tekst.recenice]
    return np.std(brojevi_tokena)

def standardnaDevBrojaRijeciURecenici(tekst):
    brojevi_rijeci = [len([t for t in nltk.word_tokenize(r) if t.isalpha()]) for r in tekst.recenice]
    return np.std(brojevi_rijeci)


# Udio složenih rečenica
def udioSlozenihRecenica(tekst):
    brojevi_veznika = [sum(1 for t in nltk.word_tokenize(r) if t.lower() in hrv_veznici)
                       for r in tekst.recenice]
    broj_slozenih = sum(1 for v in brojevi_veznika if v >= 1)
    return broj_slozenih / tekst.broj_recenica()


# Udio veznika
def udioVeznika(tekst):
    return sum(1 for t in tekst.rijeci_norm if t in hrv_veznici) / tekst.broj_tokena()
