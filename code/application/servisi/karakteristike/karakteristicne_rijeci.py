import re
import ast
import sys

from klase.tekst import Tekst
from enumi.modeli import Modeli
from enumi.skupovi import Skupovi
from servisi.podatci.tekstovi_servis import dohvatiTekstoveModela
from servisi.podatci.tekstovi_servis import dohvatiTekst



# Izračunaj omjere frekvencija riječi između generiranih i ručnih tekstova
def nadiKarakteristicneRijeci(model_id, broj_rijeci=1,
                              min_frek=10, min_broj_seminara=2, min_omjer=3):

    #dohvati sve rucne i generirane tekstove tog modela is skupa za ucenje
    rucni = dohvatiTekstoveModela(None, skup_id=Skupovi.UCENJE.skup_id)
    generirani = dohvatiTekstoveModela(model_id, skup_id=Skupovi.UCENJE.skup_id)

    #spoji generirane i rucne tekstove u dva velika teksta
    rucni_sve = Tekst(' '.join(rucni))
    generirani_sve = Tekst(' '.join(generirani))

    #odredi skup rijeci i frekvencija
    rijeci_frek = generirani_sve.n_grami_frek(broj_rijeci).most_common()

    #otvori dokument za spremanje podataka
    dokument = open('servisi/karakteristike/karakteristicne_rijeci/' 
                    + 'model ' + str(model_id) + ' - broj rijeci ' 
                    + str(broj_rijeci) + '.txt', 'w', encoding='utf-8')

    for rijec_i, gen_frek in rijeci_frek:

        #ako je frekvencija veca od najmanje dozvoljene
        if (gen_frek >= min_frek):

            #provjeri pojavljuje li se rijec samo u jednom generiranom tekstu
            #(to ukazuje da je vezano za temu specificnog seminara)
            broj_seminara = 0
            for gen in generirani:
                if(Tekst(gen).n_grami_frek(broj_rijeci).get(rijec_i, 0) > 0):
                    broj_seminara += 1
                if(broj_seminara >= min_broj_seminara):
                    break

            if(broj_seminara >= min_broj_seminara):
                
                #izracunaj omjer frekvencija
                rucna_frek = rucni_sve.n_grami_frek(broj_rijeci).get(rijec_i, 0)
                omjer = gen_frek / (rucna_frek + sys.float_info.min)

                #ako je omjer veci od najmanjeg dozvoljenog
                if(omjer >= min_omjer):
                    #rijec/rijeci, generirana frekvencija, rucna frekvencija, omjer
                    dokument.write(f'{rijec_i},{gen_frek},{rucna_frek},{omjer}\n')

    dokument.close()      
        


# Izvadi karakteristicne riječi bez ponavljanja za broj riječi i sve modele
def nadiKarakteristicneRijeciPoBrojuRijeci(broj_rijeci=1, modeli=list(Modeli)[1:]):

    #napravi set za karakteristicne rijeci/sintagme
    rijec_i = set()
    
    #za sve modele
    for model in modeli:
            
        #procitaj sve redove
        dokument = open('servisi/karakteristike/karakteristicne_rijeci/' 
                + 'model ' + str(model.model_id) + ' - broj rijeci ' 
                + str(broj_rijeci) + '.txt', 'r', encoding='utf-8')
        redovi = dokument.readlines()
        dokument.close() 

        #izvadi rijeci/i iz ostatka teksta izmedu znakova
        for red in redovi:
            rijec = re.search('\((.*)\)', red).group(0)
            rijec_i.add(rijec)

        #zapisi rijeci iz rijecnika u dokument
        dokument = open('servisi/karakteristike/karakteristicne_rijeci/sve/' 
                        + str(broj_rijeci) + '.txt', 'w', encoding='utf-8')
        for r in rijec_i:
            dokument.write(f'{r}\n')

    dokument.close()



# Udio karakterističnih riječi i sintagmi
def udioKarakteristicnihRijeci(tekst, broj_rijeci):

    #otvori dokument sa karakteristicnim rijecima ili sintagmama
    dokument = open('servisi/karakteristike/karakteristicne_rijeci/sve/'
                    + str(broj_rijeci) + '.txt', 'r', encoding='utf-8')
    redci = dokument.readlines()

    #zbroji frekvencije svih rijeci 
    frek = 0
    for redak in redci:
        rijec_i = ast.literal_eval(redak.strip())
        frek += tekst.n_grami_frek(broj_rijeci).get(rijec_i, 0)

    return frek / tekst.broj_rijeci()



# Dohvati sve karakteristične riječi i sintagme
def listaKarakteristicnihRijeci(tekst_id):

    #dohvati tekst
    tekst = Tekst(dohvatiTekst(tekst_id))

    #lista sa svim rijecima i sintagmama
    rijec_i = []

    for broj_rijeci in range(3, 0, -1):
        dokument = open('servisi/karakteristike/karakteristicne_rijeci/sve/'
                    + str(broj_rijeci) + '.txt', 'r', encoding='utf-8')
        redci = dokument.readlines()

        #ako je frekvencija veca od 0, dodaj rijec/i
        for redak in redci:
            rijec = ast.literal_eval(redak.strip())
            frek = tekst.n_grami_frek(broj_rijeci).get(rijec, 0)
            if(frek > 0):
                rijec_i.append(' '.join(rijec))

    return rijec_i



# Dohvati sve primjere direktnih odgovora na upit
def listaRijeciZaNaivniTest():

    #procitaj rijeci koje odgovaraju na upit
    dokument = open('servisi/karakteristike/karakteristicne_rijeci/sve/'
                    + 'naivni_test' + '.txt', 'r', encoding='utf-8')
    redci = dokument.readlines()

    rijeci = []
    for redak in redci:
        rijeci.append(redak.strip())
        
    return rijeci
