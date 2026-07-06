import sqlite3
import numpy as np

from enumi.modeli import Modeli
from enumi.kategorije import Kategorije

from enumi.karakteristike_funkcije import KarakteristikeFunkcije

from servisi.podatci.analize_modela_servis import kreirajAnalizeModela



# Izračunaj kojoj je granici bliže (0 za ručni tekst, 1 za generirani)
def predikcija(nepoznata, rucna_granica, generirana_granica):
    rucna_udaljenost = np.abs(nepoznata - rucna_granica)
    generirana_udaljenost = np.abs(nepoznata - generirana_granica)
    #ako su i rucna i generirana udaljenost nula, onda je neodluceno
    if(rucna_udaljenost + generirana_udaljenost == 0):
        return 0.5
    else:
        return rucna_udaljenost / (rucna_udaljenost + generirana_udaljenost)



# Napravi predikcije za određenu karakteristiku za sve modele
def predikcijeZaKarakteristiku(nepoznata, karakteristika_id, modeli=list(Modeli)[1:]):

    #rjecnik za predikcije razlicitih modela
    predikcije = {}

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    for model in modeli:
        
        #dohvati granice za rucne i generirane tekstove
        c.execute("""
        SELECT vrijednost_prosjek
        FROM granice
        WHERE model_id IS ?
        AND karakteristika_id = ?""", 
        (None, karakteristika_id))
        rucna = c.fetchone()['vrijednost_prosjek']

        c.execute("""
        SELECT vrijednost_prosjek
        FROM granice
        WHERE model_id IS ?
        AND karakteristika_id = ?""", 
        (model.model_id, karakteristika_id))
        generirana = c.fetchone()['vrijednost_prosjek']

        #izracunaj vjerojatnost da je nepoznata vrijednost bliza generiranoj granici
        vjerojatnost = predikcija(nepoznata, rucna, generirana)

        #spremi vjerojatnost u rjecnik
        predikcije[model.model_id] = vjerojatnost

    conn.close()

    return predikcije



# Napravi predickije za određene karakteristike
def predikcijeZaKarakteristike(tekst_id, karakteristike=KarakteristikeFunkcije.getIds()):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #rjecnik za sve predikcije
    rjecnici = {}

    for karakteristika in karakteristike:

        #dohvati vrijednost karakteristike za tekst
        c.execute("""
        SELECT vrijednost FROM karakteristike_teksta
        WHERE tekst_id = ? AND karakteristika_id = ?""",
        (tekst_id, karakteristika))
        vrijednost = c.fetchone()['vrijednost']

        #izracunaj predikcije za karakteristiku
        predikcije = predikcijeZaKarakteristiku(vrijednost, karakteristika)
        rjecnici[karakteristika] = predikcije

    conn.close()
    
    return rjecnici



# Izračunaj prosječnu predikciju za sve karakteristike
def predikcijeZaKarakteristikeProsjek(tekst_id):

    #dohvati rjecnike sa predikcijama modela za sve karakteristike
    rjecnici = predikcijeZaKarakteristike(tekst_id)

    #rjecnik za izracunate prosjecne predikcije karakteristika
    predikcije_karakteristika = {}

    #za sve karakteristike izracunaj konacnu vrijednost
    for karakteristika in rjecnici.keys():

        #izracunaj prosjecnu vjerojatnost
        predikcije = np.array(list(rjecnici[karakteristika].values()))
        vjerojatnost = np.sum(predikcije) / len(predikcije)
        predikcije_karakteristika[karakteristika] = vjerojatnost

    return predikcije_karakteristika



# PREDICKIJA ZA KATEGORIJU

# Napravi predikcije za sve karakteristike iste kategorije
def predikcijeZaKategoriju(tekst_id, kategorija_id):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #dohvati sve karakteristike neke kategorije
    c.execute("""
    SELECT karakteristika_id
    FROM karakteristike
    WHERE kategorija_id = ?""", 
    (kategorija_id,))

    #napravi listu za karakteristike
    redci = c.fetchall()
    karakteristike = [redak['karakteristika_id'] for redak in redci]

    #dohvati rjecnik s rjecnicima predikcija za kategorije
    rjecnici = predikcijeZaKarakteristike(tekst_id, karakteristike)
    
    return rjecnici



# Izračunaj ukupnu predikciju svake karakteristike za neku kategoriju
def predikcijeKarakteristikaZaKategoriju(tekst_id, kategorija_id):
    
    #dohvati rjecnike sa predikcijama modela za sve karakteristike
    rjecnici = predikcijeZaKategoriju(tekst_id, kategorija_id)

    #rjecnik za izracunate prosjecne predikcije karakteristika
    predikcije_kategorije = {}

    #za sve karakteristike izracunaj konacnu vrijednost
    for karakteristika in rjecnici.keys():

        #izracunaj prosjecnu vjerojatnost
        predikcije = np.array(list(rjecnici[karakteristika].values()))
        vjerojatnost = np.sum(predikcije) / len(predikcije)  
        predikcije_kategorije[karakteristika] = vjerojatnost

    return predikcije_kategorije



# Izračunaj prosječnu predikciju za kategoriju
def predikcijaZaKategoriju(tekst_id, kategorija_id):
    predikcije = predikcijeKarakteristikaZaKategoriju(tekst_id, kategorija_id)
    predikcija_kategorije = np.average(list(predikcije.values()))
    return predikcija_kategorije



# PREDIKCIJA ZA MODEL

# Izračunaj prosječnu predikciju za model
def predikcijaZaModel(tekst_id, model_id, karakteristike=KarakteristikeFunkcije.getIds()):

    #dohvati rjecnik s rjecnicima predikcija za kategorije
    rjecnici = predikcijeZaKarakteristike(tekst_id, karakteristike)

    #zbroj predikcija karakterisitka za modela
    zbroj = 0

    #pribroji predikcije za model
    for karakteristika in rjecnici.keys():
        zbroj += rjecnici[karakteristika][model_id]

    #izracunaj predikciju modela
    predikcija_modela = zbroj / len(karakteristike)

    return predikcija_modela



# Provjeri jesu li sve predikcije modela niže od praga
def predikcijeSvihModelaManjeOdPraga(pred_modeli, prag=0.5):
    for pred_model in pred_modeli:
        if(pred_model > prag):
            return False
    return True



# PREDIKCIJA UKUPNO

# Napravi analizu i vrati sve bitne podatke
def napraviAnalizu(tekst_id, prag=0.5):

    #rjecnik za bitne podatke
    podatci = {}
    
    #dohvati predikcije za sve kategorije
    kategorije = []
    for kategorija in Kategorije:
        kategorije.append(predikcijaZaKategoriju(tekst_id, kategorija.kategorija_id))
    podatci['kategorije'] = kategorije

    #dohvati predikcije za sve modele
    modeli = []
    for model in list(Modeli)[1:]:
        modeli.append(predikcijaZaModel(tekst_id, model.model_id))
    podatci['modeli'] = modeli

    #izracunaj prosjecne vjerojatnosti za kategorije i modele
    prosjek_kategorije = np.average(kategorije)
    prosjek_modeli = np.average(modeli)
    prosjek = np.average([prosjek_kategorije, prosjek_modeli])
    podatci['prosjek'] = prosjek

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #dohvati ispravnu vrijednost za tekst
    c.execute("SELECT generirano FROM tekstovi WHERE tekst_id = ?", (tekst_id,))
    redak = c.fetchone()
    vrijednost_stvarna = redak['generirano']

    #ako je predikcija za sve modele manja od praga, tekst je rucno napisan
    if(predikcijeSvihModelaManjeOdPraga(modeli, prag)):
        predikcija_da_ne = 0
    else:
        predikcija_da_ne = 1
    podatci['predikcija_da_ne'] = predikcija_da_ne

    #ako predvidena i stvarna vrijednost nisu iste, predikcija nije tocna 
    if(vrijednost_stvarna != predikcija_da_ne):
        predikcija_tocno = 0
    else:
        predikcija_tocno = 1
    podatci['predikcija_tocno'] = predikcija_tocno

    #nadi koji je model najvjerojatniji
    pred_max_model = np.max(modeli)
    podatci['pred_max_model'] = pred_max_model
    pred_model_id = modeli.index(pred_max_model) + 1
    podatci['pred_model_id'] = pred_model_id

    conn.close()

    return podatci



# Kreiraj novi redak u tablici analize
def kreirajAnalizu(tekst_id, prag=0.5):

    podatci = napraviAnalizu(tekst_id, prag)

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #dohvati analizu ako postoji
    c.execute("SELECT analiza_id FROM analize WHERE tekst_id = ?", (tekst_id,))
    redak = c.fetchone()

    #ako postoji, azuriraj je, ako ne, stvori je
    if(redak != None):
        c.execute("""
        UPDATE analize
        SET pred_sintakticka = ?,
            pred_semanticka = ?,
            pred_stilisticka = ?,
            pred_prosjek = ?,
            predikcija_da_ne = ?,
            predikcija_tocno = ?,
            pred_model_id = ?,
            pred_max_model = ?
        WHERE tekst_id = ?""",
        (podatci['kategorije'][0], podatci['kategorije'][1], podatci['kategorije'][2], 
        podatci['prosjek'], podatci['predikcija_da_ne'], podatci['predikcija_tocno'],
        podatci['pred_model_id'], podatci['pred_max_model'],
        tekst_id))

    else:
        c.execute("""
        INSERT INTO analize (tekst_id,
                            pred_sintakticka, pred_semanticka, pred_stilisticka,
                            pred_prosjek, predikcija_da_ne, predikcija_tocno,
                            pred_model_id, pred_max_model)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (tekst_id,
        podatci['kategorije'][0], podatci['kategorije'][1], podatci['kategorije'][2], 
        podatci['prosjek'], podatci['predikcija_da_ne'], podatci['predikcija_tocno'],
        podatci['pred_model_id'], podatci['pred_max_model']))

    conn.commit()

    #dohvati analiza_id za analizu
    c.execute("SELECT analiza_id FROM analize WHERE tekst_id = ?", (tekst_id,))
    redak = c.fetchone()

    conn.close()

    #kreiraj retke u tablici analize_modela
    kreirajAnalizeModela(redak['analiza_id'], podatci['modeli'])
