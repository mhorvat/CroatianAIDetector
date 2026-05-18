import sqlite3

from enumi.modeli import Modeli
from enumi.skupovi import Skupovi
from klase.zahtjev_tekst import ZahtjevTekst



# Kreiraj novi redak u tablici tekstovi
def kreirajTekst(zahtjev_tekst):

    conn = sqlite3.connect('./db/a10a.db')
    c = conn.cursor()

    c.execute('''
    INSERT INTO tekstovi (tema, generirano, generirano_puta, skup_id, model_id, upit, tekst)
    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
    (zahtjev_tekst.tema, zahtjev_tekst.generirano, zahtjev_tekst.generirano_puta,
     zahtjev_tekst.skup_id, zahtjev_tekst.model_id,zahtjev_tekst.upit, zahtjev_tekst.tekst))
    
    conn.commit()
    conn.close()



# Dohvati zadnji tekst_id u tablici tekstovi
def zadnjiTekstId():

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('SELECT MAX(tekst_id) AS tekst_id FROM tekstovi')
    redak = c.fetchone()
    
    conn.close()

    return redak['tekst_id']



# Spremi tekst u bazu
def spremiTekst(ime, upit=None, skup_id=1, model_id=None,
                tema=None, generirano=0, generirano_puta=None):

    #ako nema posebne teme, ista je kao ime
    if(tema == None):
        tema = ime

    #postavi skup dio putanje (ucenje ili ispitivanje)
    if(skup_id == Skupovi.UCENJE.skup_id):
        skup = Skupovi.UCENJE.naziv
    elif(skup_id == Skupovi.ISPITIVANJE.skup_id):
        skup = Skupovi.ISPITIVANJE.naziv

    putanja = None
    #postavi putanju prema modelu
    if(model_id == None):
        putanja = 'seminari/' + skup + '/rucni/'
    elif(model_id == Modeli.CHAT_GPT.model_id):
        putanja = 'seminari/' + skup + '/generirani/chatgpt/'
    elif(model_id == Modeli.CLAUDE.model_id):
        putanja = 'seminari/' + skup + '/generirani/claude/'
    elif(model_id == Modeli.GEMINI.model_id):
        putanja = 'seminari/' + skup + '/generirani/gemini/'

    if(putanja != None):
        #spremi u bazu
        zahtjev = ZahtjevTekst(tema=tema, 
                               generirano=generirano, 
                               generirano_puta=generirano_puta,
                               skup_id=skup_id, 
                               model_id=model_id, 
                               upit=upit,
                               putanja=putanja + ime + '.txt')
        kreirajTekst(zahtjev)



# Spremi ručne i sve generirane tekstove na neku temu
def spremiRucneIGeneriraneTekstove(ime, upit, skup_id=1, 
                                   modeli=Modeli, tema=None):
    for model in modeli:
        if(model.model_id == None):
            spremiTekst(ime, upit=None, skup_id=skup_id,
                        model_id=model.model_id, tema=tema)
        else:
            spremiTekst(ime, upit=upit, skup_id=skup_id,
                        model_id=model.model_id, tema=tema,
                        generirano=1)



# Dohvati sve tekstove istog modela u nekom skupu
def dohvatiTekstoveModela(model_id, skup_id=1):

    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT tekst FROM tekstovi WHERE model_id IS ? AND skup_id = ?",
    (model_id, skup_id))
    redci = c.fetchall()
    conn.close()

    return [redak['tekst'] for redak in redci]



# Dohvati tekst za neki tekst_id
def dohvatiTekst(tekst_id):
    conn = sqlite3.connect('./db/a10a.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT tekst FROM tekstovi WHERE tekst_id = ?', (tekst_id,))
    redak = c.fetchone()
    conn.close()
    return redak['tekst']
