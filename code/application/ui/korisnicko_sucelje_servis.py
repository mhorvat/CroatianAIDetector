from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt

from enumi.modeli import Modeli
from enumi.skupovi import Skupovi
from klase.zahtjev_tekst import ZahtjevTekst

from servisi.podatci.tekstovi_servis import kreirajTekst
from servisi.podatci.karakteristike_teksta_servis import kreirajKarakteristikeTeksta
from servisi.podatci.analize_servis import kreirajAnalizu

from servisi.podatci.analize_servis import napraviAnalizu
from servisi.podatci.analize_servis import predikcijeZaKarakteristikeProsjek



# Spremi tekst iz podataka korisničkog sučelja i vrati tekst_id
def spremiTekstIzPodatakaSucelja(naslov, generirano, generirano_puta, model, upit, 
                                 tekst_ili_putanja, putanja):

    #postavi skup_id na Proba
    skup_id = Skupovi.PROBA.skup_id

    #postavi model_id
    if(not generirano):
        model_id = Modeli.COVJEK.model_id
    elif(model == Modeli.CHAT_GPT.naziv):
        model_id = Modeli.CHAT_GPT.model_id
    elif(model == Modeli.CLAUDE.naziv):
        model_id = Modeli.CLAUDE.model_id
    elif(model == Modeli.GEMINI.naziv):
        model_id = Modeli.GEMINI.model_id

    #ako je putanja, procitaj tekst iz nje, inace je tekst
    if(putanja):
        tekst = open(tekst_ili_putanja, encoding='utf-8').read()
    else:
        tekst = tekst_ili_putanja
        
    #napravi zahtjev za spremanje teksta
    zahtjev = ZahtjevTekst(tema=naslov, 
                           generirano=generirano, 
                           generirano_puta=generirano_puta,
                           skup_id=skup_id, 
                           model_id=model_id, 
                           upit=upit,
                           tekst=tekst)
    
    #spremi tekst
    kreirajTekst(zahtjev)
        


# Izračunaj karakteristike, napravi analizu i vrati rezultate
def analizirajTekst(tekst_id):

    #izracunaj vrijednosti svih karakteristika za tekst
    kreirajKarakteristikeTeksta(tekst_id)

    #izracunaj analizu
    kreirajAnalizu(tekst_id)
    podatci = napraviAnalizu(tekst_id)
    karakteristike = predikcijeZaKarakteristikeProsjek(tekst_id)

    #povezi podatke u jedan rjecnik
    podatci.update(karakteristike)

    return podatci
