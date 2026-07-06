import nltk



# Klasa ZahtjevTekst
class ZahtjevTekst:
    def __init__(self, tema, generirano, skup_id, model_id, upit,
                 generirano_puta=None, tekst=None, putanja=None):
        
        self.tema = tema
        self.generirano = generirano

        if (generirano_puta == None):
            if (generirano == 0):
                self.generirano_puta = None
            else:
                self.generirano_puta = 1
        else:
            self.generirano_puta = generirano_puta
        
        self.skup_id = skup_id
        self.model_id = model_id
        self.upit = upit
        
        if (tekst != None):
            self.tekst = tekst
        elif (putanja != None):
            self.tekst = open(putanja, encoding='utf-8').read()
        else:
            self.tekst = None
