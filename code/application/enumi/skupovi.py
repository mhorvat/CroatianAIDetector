from enum import Enum



# Enum Skupovi
class Skupovi(Enum):
    UCENJE = (1, 'ucenje')
    ISPITIVANJE = (2, 'ispitivanje')
    PROBA = (3, 'proba')


    def __init__(self, skup_id, naziv):
        self.skup_id = skup_id
        self.naziv = naziv
