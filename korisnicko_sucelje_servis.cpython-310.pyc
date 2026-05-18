import sqlite3

from klase.tekst import Tekst
from enumi.karakteristike_funkcije import KarakteristikeFunkcije



# Kreiraj novi redak u tablici karakteristike_teksta
def kreirajKarakteristikeTeksta(tekst_id, funkcije=KarakteristikeFunkcije):

      conn = sqlite3.connect('./db/a10a.db')
      conn.row_factory = sqlite3.Row
      c = conn.cursor()

      #dohvati tekst
      c.execute("SELECT tekst FROM tekstovi WHERE tekst_id = ?", (tekst_id,))
      redak = c.fetchone()
      tekst = Tekst(redak['tekst'])

      #idi kroz funkcije za racunanje vrijednosti karakteristika
      for kf in funkcije:
            karakteristika_id = kf.karakteristika_id
            vrijednost = kf.funkcija(tekst)

            #dohvati karakteristiku teksta ako postoji
            c.execute("""
            SELECT karakteristika_teksta_id FROM karakteristike_teksta
            WHERE tekst_id = ? AND karakteristika_id = ?""",
            (tekst_id, karakteristika_id))
            redak = c.fetchone()

            #ako postoji, azuriraj je, ako ne, stvori je
            if(redak != None):
                  c.execute("""
                  UPDATE karakteristike_teksta SET vrijednost = ?
                  WHERE tekst_id = ? AND karakteristika_id = ?""",
                  (vrijednost, tekst_id, karakteristika_id))
            else:
                  c.execute("""
                  INSERT INTO karakteristike_teksta
                  (tekst_id, karakteristika_id, vrijednost)
                  VALUES (?, ?, ?)""", 
                  (tekst_id, karakteristika_id, vrijednost))
          
      conn.commit()
      conn.close()
