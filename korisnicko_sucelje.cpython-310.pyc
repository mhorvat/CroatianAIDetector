import sqlite3
import numpy as np

from enumi.skupovi import Skupovi
from enumi.modeli import Modeli
from enumi.karakteristike_funkcije import KarakteristikeFunkcije



# Kreiraj novi redak u tablici granice
def kreirajGranicu(model_id, karakteristika_id):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #dohvati sve redke u tablici karakteristike_teksta za model_id i karakteristika_id
    c.execute("""
    SELECT tekstovi.tekst_id, vrijednost
    FROM karakteristike_teksta
    JOIN tekstovi ON karakteristike_teksta.tekst_id = tekstovi.tekst_id
    WHERE skup_id = ?
    AND model_id IS ?
    AND karakteristika_id = ?""", 
    (Skupovi.UCENJE.skup_id, model_id, karakteristika_id))
    
    #napravi liste za vrijednosti i tekst_idjeve
    redci = c.fetchall()
    vrijednosti = [redak['vrijednost'] for redak in redci]
    tekst_ids  = [redak['tekst_id'] for redak in redci]

    #nadi prosjek, medijan, std, min, max
    prosjek = np.mean(vrijednosti)
    medijan = np.median(vrijednosti)
    std = np.std(vrijednosti)
    mini = np.min(vrijednosti)
    maxi = np.max(vrijednosti)

    #nadi broj podataka, tekst_id koji ima najmanju i najvecu vrijednost 
    broj_podataka = len(vrijednosti)
    tekst_min = tekst_ids[vrijednosti.index(mini)]
    tekst_max = tekst_ids[vrijednosti.index(maxi)]

    #dohvati granicu ako postoji
    c.execute("""
    SELECT granica_id FROM granice
    WHERE model_id IS ?
    AND karakteristika_id = ?""",
    (model_id, karakteristika_id))
    redak = c.fetchone()

    #ako granica postoji, azuriraj je, ako ne, stvori je
    if(redak != None):
        c.execute("""
        UPDATE granice
        SET broj_podataka = ?,
            vrijednost_prosjek = ?,
            vrijednost_medijan = ?,
            vrijednost_std = ?,
            vrijednost_min = ?,
            vrijednost_max = ?,
            tekst_id_min = ?,
            tekst_id_max = ?
        WHERE model_id IS ?
        AND karakteristika_id = ?""",
        (broj_podataka, prosjek, medijan, std, mini, maxi, tekst_min, tekst_max,
        model_id, karakteristika_id))
    
    else:
        c.execute("""
        INSERT INTO granice (model_id, karakteristika_id, broj_podataka,
                            vrijednost_prosjek, vrijednost_medijan, vrijednost_std,
                            vrijednost_min, vrijednost_max,
                            tekst_id_min, tekst_id_max)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
        (model_id, karakteristika_id,
        broj_podataka, prosjek, medijan, std, mini, maxi, tekst_min, tekst_max))

    conn.commit()
    conn.close()



# Kreiraj sve granice za sve modele za sve karakteristike
def kreirajSveGranice(modeli=Modeli, karakteristike=KarakteristikeFunkcije):
    for model in modeli:
        for karakteristika in karakteristike:
            kreirajGranicu(model.model_id, karakteristika.karakteristika_id)
            