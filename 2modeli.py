import sqlite3

conn = sqlite3.connect('db/a10a.db')
c = conn.cursor()



c.execute("""
INSERT INTO skupovi (skup_id, skup_naziv)
VALUES 
    (1, 'Učenje'),
    (2, 'Ispitivanje'),
    (3, 'Proba');
""")



conn.commit()
conn.close()
