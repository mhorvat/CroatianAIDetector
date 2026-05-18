import sqlite3

conn = sqlite3.connect('db/a10a.db')
c = conn.cursor()



c.execute("""
INSERT INTO kategorije (kategorija_id, kategorija_naziv)
VALUES 
    (1, 'Sintaktička'),
    (2, 'Semantička'),
    (3, 'Stilistička');
""")



conn.commit()
conn.close()
