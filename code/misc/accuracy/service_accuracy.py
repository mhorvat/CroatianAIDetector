import sqlite3

from servisi.podatci.analize_servis import predikcijaZaKategoriju
from servisi.podatci.analize_servis import predikcijeZaKarakteristikeProsjek



# Dohvati ukupnu točnost modela
def ukupnaTocnost():
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
    SELECT SUM(predikcija_tocno) * 1.0 / COUNT(*) AS tocnost 
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id 
    WHERE skup_id != 3""")
    tocnost = c.fetchone()['tocnost']
    conn.close()
    return tocnost



# Dohvati točnost modela za određeni skup
def tocnostZaSkup(skup_id):
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
    SELECT SUM(predikcija_tocno) * 1.0 / COUNT(*) AS tocnost
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id 
    WHERE skup_id = ?""",
    (skup_id,))

    tocnost = c.fetchone()['tocnost']
    conn.close()
    return tocnost



# Dohvati točnost modela za određeni model
def tocnostZaModel(model_id):
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
    SELECT SUM(predikcija_tocno) * 1.0 / COUNT(*) AS tocnost
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id 
    WHERE model_id IS ?
    AND skup_id != 3""",
    (model_id,))

    tocnost = c.fetchone()['tocnost']
    conn.close()
    return tocnost



# Dohvati točnost modela za određenu kategoriju
def tocnostZaKategoriju(kategorija_id, prag=0.5):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #broj tocnih predikcija
    tocni = 0

    #dohvati sve tekstove
    c.execute("SELECT tekst_id, generirano FROM tekstovi WHERE skup_id != 3")
    redci = c.fetchall()
    conn.close()

    #idi kroz tekstove
    for redak in redci:
        #dohvati predikciju kategorije za tekst i kategoriju
        predikcija_kategorije = predikcijaZaKategoriju(redak['tekst_id'], kategorija_id)
        
        #ako tekst nije generiran, predikcija treba biti manja od praga
        if(redak['generirano'] == 0):
            if(predikcija_kategorije <= prag):
                tocni += 1
        else:
            if(predikcija_kategorije > prag):
                tocni += 1

    return tocni / len(redci)



# Dohvati točnost modela za sve karakteristike
def tocnostZaKarakteristike(prag=0.5):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #rjecnik za broj tocnih predikcija po karakteristici
    tocni = {}

    #dohvati sve tekstove
    c.execute("SELECT tekst_id, generirano FROM tekstovi WHERE skup_id != 3")
    redci = c.fetchall()
    conn.close()

    #idi kroz tekstove
    for redak in redci:

        #dohvati predikcije karakteristika za sve kategorije
        predikcije = predikcijeZaKarakteristikeProsjek(redak['tekst_id'])
        
        #idi kroz predikcije svih karakteristika za jedan tekst
        for karakteristika_id in predikcije.keys():
            predikcija_karakteristike = predikcije[karakteristika_id]

            #ako karakteristika_id vec postoji u rjecniku tocnih,
            #dohvati dosadasnji broj tocnih
            if(karakteristika_id in tocni.keys()):
                tocni_dosad = tocni[karakteristika_id]
            else:
                tocni_dosad = 0

            #ako tekst nije generiran, predikcija treba biti manja od praga
            if(redak['generirano'] == 0):
                if(predikcija_karakteristike <= prag):
                    tocni_dosad += 1
            else:
                if(predikcija_karakteristike > prag):
                    tocni_dosad += 1

            #dodaj karakteristiku i broj tocnih u rjecnik
            tocni[karakteristika_id] = tocni_dosad

    #rjecnik za tocnosti karakteristika
    tocnosti = {}
    for karakteristika_id in tocni.keys():
        tocnosti[karakteristika_id] = tocni[karakteristika_id] / len(redci)

    return tocnosti



# Dohvati točnost odabira najvjerojatnijeg modela
def tocnostZaNajvjerojatnijiModel():
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
    WITH redci_tocni (tocni) AS
    (SELECT COUNT(*) AS tocni
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
    WHERE pred_model_id = model_id
    AND skup_id != 3),

    redci_svi (svi) AS 
    (SELECT COUNT(*) AS svi 
	FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
	WHERE skup_id != 3),

    redci_tocni_rucni (tocni_rucni) AS
    (SELECT COUNT(*) AS tocni_rucni
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
    WHERE predikcija_tocno = 1 AND model_id IS NULL
	AND skup_id != 3)

    SELECT tocni * 1.0 / (svi - tocni_rucni) AS tocnost
    FROM redci_tocni
    JOIN redci_svi
    JOIN redci_tocni_rucni""")

    tocnost = c.fetchone()['tocnost']
    conn.close()
    return tocnost



# Dohvati točnost nekog modela ako je odabran
def tocnostZaOdabraniModel(model_id):
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("""
    WITH redci_tocni (tocni) AS
    (SELECT COUNT(*) AS tocni
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
    WHERE pred_model_id = model_id
	AND pred_model_id = ?
    AND skup_id != 3),

    redci_svi (svi) AS
    (SELECT COUNT(*) AS svi 
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
	WHERE pred_model_id = ?
    AND skup_id != 3),

    redci_tocni_rucni (tocni_rucni) AS
    (SELECT COUNT(*) AS tocni_rucni
    FROM analize JOIN tekstovi ON analize.tekst_id = tekstovi.tekst_id
    WHERE predikcija_tocno = 1
	AND model_id IS NULL
	AND pred_model_id = ?
    AND skup_id != 3)

    SELECT tocni * 1.0 / (svi - tocni_rucni) AS tocnost
    FROM redci_tocni
    JOIN redci_svi
    JOIN redci_tocni_rucni""",
    (model_id, model_id, model_id))

    tocnost = c.fetchone()['tocnost']
    conn.close()
    return tocnost
