import string

from servisi.karakteristike.karakteristicne_rijeci import udioKarakteristicnihRijeci



# Varijable
hrv_pun = ['„', '“', '”', '…', '–', '—']



# STILISTIČKE

# Prosječna duljina riječi
def prosjecnaDuljinaTokena(tekst):
    return sum(len(t) for t in tekst.tokeni) / tekst.broj_tokena()

def prosjecnaDuljinaRijeci(tekst):
    return sum(len(t) for t in tekst.rijeci) / tekst.broj_rijeci()


# Udio riječi s velikim početnim slovom u naslovima potpoglavlja
def udioTokenaUTitluPotpoglavlja(tekst):
    return sum(1 for t in tekst.tokeni if t.istitle()) / tekst.broj_tokena() 


# Udio interpunkcijskih znakova 
def udioInterpunkcija(tekst):
    return sum(1 for t in tekst.tokeni if t in string.punctuation or t in hrv_pun) / tekst.broj_tokena() 


# Udio en-crta
def udioEnCrta(tekst):
    return tekst.frek['–'] / tekst.broj_tokena()


# Udio em-crta
def udioEmCrta(tekst):
    return tekst.frek['—'] / tekst.broj_tokena()


# Udio dvotočaka
def udioDvotocaka(tekst):
    return tekst.frek[':'] / tekst.broj_tokena()


# Udio zagrada
def udioZagrada(tekst):
    return (tekst.frek['('] + tekst.frek[')']) / tekst.broj_tokena()


# Udio stranih dvostrukih navodnika
def udioStranihNavodnika(tekst):
    strani = tekst.frek['”'] #znak “ koristi se i u hrvatskom, ali za zatvaranje
    hrvatski = tekst.frek['„'] #znak “ koristi se i u engleskom, ali za otvaranje
    navodnici = strani + hrvatski
    if (navodnici != 0):
        return strani / (navodnici)
    else:
        return 0



# KARAKTERISTIČNE RIJEČI

# Udio karakterističnih riječi i sintagmi
def udioKarakteristicnihRijeci1(tekst):
    return udioKarakteristicnihRijeci(tekst=tekst, broj_rijeci=1)

def udioKarakteristicnihRijeci2(tekst):
    return udioKarakteristicnihRijeci(tekst=tekst, broj_rijeci=2)

def udioKarakteristicnihRijeci3(tekst):
    return udioKarakteristicnihRijeci(tekst=tekst, broj_rijeci=3)
