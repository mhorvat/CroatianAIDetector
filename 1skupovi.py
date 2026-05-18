import sqlite3

conn = sqlite3.connect('db/a10a.db')
c = conn.cursor()



# Tablica skupovi
c.execute("""
CREATE TABLE IF NOT EXISTS skupovi (
    skup_id INTEGER PRIMARY KEY,
    skup_naziv TEXT
);
""")


# Tablica modeli
c.execute("""
CREATE TABLE IF NOT EXISTS modeli (
    model_id INTEGER PRIMARY KEY,
    model_naziv TEXT,
    model_verzija TEXT
);
""")


# Tablica kategorije
c.execute("""
CREATE TABLE IF NOT EXISTS kategorije (
    kategorija_id INTEGER PRIMARY KEY,
    kategorija_naziv TEXT
);
""")


# Tablica karakteristike
c.execute("""
CREATE TABLE IF NOT EXISTS karakteristike (
    karakteristika_id INTEGER PRIMARY KEY,
    kategorija_id INTEGER,
    karakteristika_naziv TEXT,
    opis TEXT,
    FOREIGN KEY (kategorija_id) REFERENCES kategorije(kategorija_id)
);
""")



# Tablica tekstovi
c.execute("""
CREATE TABLE IF NOT EXISTS tekstovi (
    tekst_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tema TEXT,
    generirano INTEGER,
    generirano_puta INTEGER,
    skup_id INTEGER,
    model_id INTEGER,
    upit TEXT,
    tekst TEXT,
    datum_izrade DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (skup_id) REFERENCES skupovi(skup_id),
    FOREIGN KEY (model_id) REFERENCES modeli(model_id)
);
""")


# Tablica karakteristike_teksta
c.execute("""
CREATE TABLE IF NOT EXISTS karakteristike_teksta (
    karakteristika_teksta_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tekst_id INTEGER,
    karakteristika_id INTEGER,
    vrijednost REAL,
    FOREIGN KEY (tekst_id) REFERENCES tekstovi(tekst_id),
    FOREIGN KEY (karakteristika_id) REFERENCES karakteristike(karakteristika_id)
);
""")


# Tablica granice
c.execute("""
CREATE TABLE IF NOT EXISTS granice (
    granica_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    karakteristika_id INTEGER,
    broj_podataka INTEGER,
    vrijednost_prosjek REAL,
    vrijednost_medijan REAL,
    vrijednost_std REAL,
    vrijednost_min REAL,
    vrijednost_max REAL,
    tekst_id_min INTEGER,
    tekst_id_max INTEGER,
    FOREIGN KEY (model_id) REFERENCES modeli(tekst_id),
    FOREIGN KEY (tekst_id_min) REFERENCES tekstovi(tekst_id),
    FOREIGN KEY (tekst_id_max) REFERENCES tekstovi(tekst_id)
);
""")


# Tablica analize
c.execute("""
CREATE TABLE IF NOT EXISTS analize (
    analiza_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tekst_id INTEGER,
    pred_sintakticka REAL,
    pred_semanticka REAL,
    pred_stilisticka REAL,
    pred_prosjek REAL,
    predikcija_da_ne INTEGER,
    predikcija_tocno INTEGER,
    pred_model_id INTEGER,
    pred_max_model REAL,
    FOREIGN KEY (tekst_id) REFERENCES tekstovi(tekst_id),
    FOREIGN KEY (pred_model_id) REFERENCES modeli(model_id)
);
""")



# Tablica analize_modela
c.execute("""
CREATE TABLE IF NOT EXISTS analize_modela (
    analiza_modela_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analiza_id INTEGER,
    model_id INTEGER,
    predikcija REAL,
    FOREIGN KEY (analiza_id) REFERENCES analize(analiza_id),
    FOREIGN KEY (model_id) REFERENCES modeli(model_id)
);
""")



conn.commit()
conn.close()
