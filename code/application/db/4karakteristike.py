import sqlite3

conn = sqlite3.connect('db/a10a.db')
c = conn.cursor()



c.execute("""
INSERT INTO karakteristike (karakteristika_id, kategorija_id, karakteristika_naziv, opis)
VALUES 
    (1, 1, 'Prosječan broj tokena u rečenici', ''),
    (2, 1, 'Prosječan broj riječi u rečenici', ''),
    (3, 1, 'Standardna devijacija broja tokena u rečenici', ''),
    (4, 1, 'Standardna devijacija broja riječi u rečenici', ''),
    (5, 1, 'Udio složenih rečenica', ''),
    (6, 1, 'Udio veznika', ''),
          
    (7, 2, 'Udio jedinstvenih tokena', ''),
    (8, 2, 'Udio jedinstvenih riječi', ''),
    (9, 2, 'Udio brojeva', ''),
          
    (10, 3, 'Prosječna duljina tokena', ''),
    (11, 3, 'Prosječna duljina riječi', ''),
    (12, 3, 'Udio riječi s velikim početnim slovom u naslovima potpoglavlja', ''),
    (13, 3, 'Udio interpunkcijskih znakova', ''),
    (14, 3, 'Udio en-crta', ''),
    (15, 3, 'Udio em-crta', ''),
    (16, 3, 'Udio dvotočaka', ''),
    (17, 3, 'Udio zagrada', ''),
    (18, 3, 'Udio stranih dvostrukih navodnika', ''),
    (19, 3, 'Udio karakterističnih riječi', ''),
    (20, 3, 'Udio karakterističnih skupova od dvije riječi', ''),
    (21, 3, 'Udio karakterističnih skupova od tri riječi', '');
""")



conn.commit()
conn.close()
