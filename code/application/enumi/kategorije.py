from enum import Enum



# Enum Kategorije
class Kategorije(Enum):
    SINTAKTICKA = (1, 'Sintaktička')
    SEMANTICKA = (2, 'Semantička')
    STILISTICKA = (3, 'Stilistička')


    def __init__(self, kategorija_id, naziv):
        self.kategorija_id = kategorija_id
        self.naziv = naziv
