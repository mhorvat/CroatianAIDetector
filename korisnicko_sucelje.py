import sqlite3



# Kreiraj novi redak u tablici analize_modela
def kreirajAnalizuModela(analiza_id, model_id, predikcija):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #dohvati analizu_modela ako postoji
    c.execute("""
    SELECT analiza_modela_id FROM analize_modela 
    WHERE analiza_id = ? AND model_id = ?""", 
    (analiza_id, model_id))
    redak = c.fetchone()

    #ako postoji, azuriraj je, ako ne, stvori je
    if(redak != None):
        c.execute("""
        UPDATE analize_modela SET predikcija = ?
        WHERE analiza_id = ? AND model_id = ?""",
        (predikcija, analiza_id, model_id))

    else:
        c.execute("""
        INSERT INTO analize_modela (analiza_id, model_id, predikcija)
        VALUES (?, ?, ?)""", 
        (analiza_id, model_id, predikcija))

    conn.commit()
    conn.close()



# Kreiraj retke u tablici analize_modela za sve modele za određenu analizu
def kreirajAnalizeModela(analiza_id, predikcije):
    for predikcija in predikcije:
        kreirajAnalizuModela(analiza_id, predikcije.index(predikcija) + 1, predikcija)
