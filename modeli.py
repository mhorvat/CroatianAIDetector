from enum import Enum

from servisi.karakteristike.sintakticke import prosjecanBrojTokenaURecenici
from servisi.karakteristike.sintakticke import prosjecanBrojRijeciURecenici
from servisi.karakteristike.sintakticke import standardnaDevBrojaTokenaURecenici
from servisi.karakteristike.sintakticke import standardnaDevBrojaRijeciURecenici
from servisi.karakteristike.sintakticke import udioSlozenihRecenica
from servisi.karakteristike.sintakticke import udioVeznika

from servisi.karakteristike.semanticke import udioJedinstvenihTokena
from servisi.karakteristike.semanticke import udioJedinstvenihRijeci
from servisi.karakteristike.semanticke import udioBrojeva

from servisi.karakteristike.stilisticke import prosjecnaDuljinaTokena
from servisi.karakteristike.stilisticke import prosjecnaDuljinaRijeci
from servisi.karakteristike.stilisticke import udioTokenaUTitluPotpoglavlja
from servisi.karakteristike.stilisticke import udioInterpunkcija
from servisi.karakteristike.stilisticke import udioEnCrta
from servisi.karakteristike.stilisticke import udioEmCrta
from servisi.karakteristike.stilisticke import udioDvotocaka
from servisi.karakteristike.stilisticke import udioZagrada
from servisi.karakteristike.stilisticke import udioStranihNavodnika
from servisi.karakteristike.stilisticke import udioKarakteristicnihRijeci1
from servisi.karakteristike.stilisticke import udioKarakteristicnihRijeci2
from servisi.karakteristike.stilisticke import udioKarakteristicnihRijeci3



# Enum KarakteristikeFunkcije
class KarakteristikeFunkcije(Enum):
    
    PROSJECAN_BROJ_TOKENA = (1, prosjecanBrojTokenaURecenici, 
                             'Prosječan broj tokena u rečenici')
    PROSJECAN_BROJ_RIJECI = (2, prosjecanBrojRijeciURecenici, 
                             'Prosječan broj riječi u rečenici')
    STD_TOKENA = (3, standardnaDevBrojaTokenaURecenici,
                  'Standardna devijacija broja tokena u rečenici')
    STD_RIJECI = (4, standardnaDevBrojaRijeciURecenici, 
                  'Standardna devijacija broja riječi u rečenici')
    UDIO_SLOZENIH_RECENICA = (5, udioSlozenihRecenica, 'Udio složenih rečenica')
    UDIO_VEZNIKA = (6, udioVeznika, 'Udio veznika')

    UDIO_JEDINSTVENIH_TOKENA = (7, udioJedinstvenihTokena, 'Udio jedinstvenih tokena')
    UDIO_JEDINSTVENIH_RIJECI = (8, udioJedinstvenihRijeci, 'Udio jedinstvenih riječi')
    UDIO_BROJEVA = (9, udioBrojeva, 'Udio brojeva')

    PROSJECNA_DULJINA_TOKENA = (10, prosjecnaDuljinaTokena, 'Prosječna duljina tokena')
    PROSJECNA_DULJINA_RIJECI = (11, prosjecnaDuljinaRijeci, 'Prosječna duljina riječi')
    UDIO_NASLOVA = (12, udioTokenaUTitluPotpoglavlja,
                    'Udio tokena u naslovima potpoglavlja')
    UDIO_INTERPUNKCIJA = (13, udioInterpunkcija, 'Udio interpunkcijskih znakova')
    UDIO_EN_CRTA = (14, udioEnCrta, 'Udio en-crta')
    UDIO_EM_CRTA = (15, udioEmCrta, 'Udio em-crta')
    UDIO_DVOTOCAKA = (16, udioDvotocaka, 'Udio dvotočaka')
    UDIO_ZAGRADA = (17, udioZagrada, 'Udio zagrada')
    UDIO_STRANIH_NAVODNIKA = (18, udioStranihNavodnika, 'Udio stranih dvostrukih navodnika')
    UDIO_KARAKTERISTICNIH_RIJECI_1 = (19, udioKarakteristicnihRijeci1,
                                      'Udio karakterističnih riječi')
    UDIO_KARAKTERISTICNIH_RIJECI_2 = (20, udioKarakteristicnihRijeci2,
                                      'Udio karakterističnih skupova od dvije riječi')
    UDIO_KARAKTERISTICNIH_RIJECI_3 = (21, udioKarakteristicnihRijeci3,
                                      'Udio karakterističnih skupova od tri riječi')


    def __init__(self, karakteristika_id, funkcija, naziv):
        self.karakteristika_id = karakteristika_id
        self.funkcija = funkcija
        self.naziv = naziv

    @classmethod
    def getIds(cls):
        return [clan.karakteristika_id for clan in cls]
    