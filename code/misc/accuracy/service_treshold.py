import sqlite3
import numpy as np

from servisi.tocnost.tocnost_servis import tocnostZaKarakteristike
from servisi.tocnost.tocnost_servis import ukupnaTocnost
from servisi.tocnost.tocnost_servis import tocnostZaSkup
from servisi.podatci.analize_servis import kreirajAnalizu

from enumi.skupovi import Skupovi

from servisi.tocnost import tocnost_servis



# Pronađi najbolji prag za konačnu odluku
def pragZaKonacnuOdluku(min_prag, max_prag, korak):

    #rjecnik za najbolji prag i njegovu tocnost
    pragovi_tocnosti = {}

    #idi kroz sve pragove
    for prag in np.arange(min_prag, max_prag, korak):

        conn = sqlite3.connect('./db/a10a.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        #dohvati sve tekstove iz skupa za ucenje
        c.execute("SELECT tekst_id FROM tekstovi WHERE skup_id = ?",
                 (Skupovi.UCENJE.skup_id,))
        redci = c.fetchall()
        conn.close()
        
        for redak in redci:
            kreirajAnalizu(redak['tekst_id'], prag)

        pragovi_tocnosti[prag] = tocnostZaSkup(1)

    return pragovi_tocnosti



# Pronađi prag za najvišu točnost za sve karakteristike
def pragZaKarakteristike(min_prag, max_prag, korak):

    #rjecnik za najbolje karakteristika
    pragovi = {}

    #idi kroz sve pragove
    for prag in np.arange(min_prag, max_prag, korak):

        #dohvati tocnosti za prag
        tocnosti = tocnostZaKarakteristike(prag)

        #ako je nova tocnost veca od najvece, azuriraj ju
        for karakteristika_id in tocnosti.keys():
            if(karakteristika_id in pragovi.keys()):
                if(tocnosti[karakteristika_id] > pragovi[karakteristika_id][1]):
                    pragovi[karakteristika_id] = [prag, tocnosti[karakteristika_id]]
            else:
                pragovi[karakteristika_id] = [prag, tocnosti[karakteristika_id]]

    return pragovi



# Pronađi najbolje tezine za funkciju ukupne vjerojatnost
def najboljiKoeficijenti(min, max, korak):

    #rjecnik za najbolje tezine
    tezine = {}

    #dokument za spremanje podataka
    dokument = open('servisi/tocnost/koefs.txt', 'w', encoding='utf-8')

    #idi kroz sve moguce kombinacije koeficijenata
    for chat_gpt in np.arange(min, max, korak):
        for claude in np.arange(min, max, korak):
            for gemini in np.arange(min, max, korak):
                for sin in np.arange(min, max, korak):
                    for sem in np.arange(min, max, korak):
                        for stil in np.arange(min, max, korak):

                            ts = [chat_gpt, claude, gemini, 1, 1, 1]
                            
                            #napravi analizu za sve tekstove
                            for i in range(1, 283):
                                kreirajAnalizu(i, koefs=ts)
                            
                            #dohvati tocnosti
                            tocnost = ukupnaTocnost()
                            tocnost_u = tocnostZaSkup(1)
                            tocnost_i = tocnostZaSkup(2)

                            dokument.write(f'{ts},{tocnost},{tocnost_u},{tocnost_i}\n')

                            #ako je nova tocnost veca od najvece, azuriraj koeficijent
                            if(len(tezine.keys()) == 0):
                                tezine['tocnost'] = tocnost
                                tezine['koefs'] = ts
                            elif(tezine['tocnost'] < tocnost):
                                tezine['tocnost'] = tocnost
                                tezine['koefs'] = ts
    
    dokument.close()       

    return tezine
