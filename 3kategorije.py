import sqlite3

conn = sqlite3.connect('db/a10a.db')
c = conn.cursor()



c.execute("""
INSERT INTO modeli (model_id, model_naziv, model_verzija)
VALUES 
    (1, 'ChatGPT', 'GPT-5'),
    (2, 'Claude', 'Sonnet 4.5'),
    (3, 'Gemini', '2.5 Flash');
""")



conn.commit()
conn.close()
