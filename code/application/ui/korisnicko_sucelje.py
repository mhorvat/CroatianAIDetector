from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt

from enumi.modeli import Modeli
from enumi.kategorije import Kategorije
from enumi.karakteristike_funkcije import KarakteristikeFunkcije

from ui.korisnicko_sucelje_servis import spremiTekstIzPodatakaSucelja
from ui.korisnicko_sucelje_servis import analizirajTekst

from servisi.podatci.tekstovi_servis import zadnjiTekstId
from servisi.karakteristike.karakteristicne_rijeci import listaKarakteristicnihRijeci
from servisi.karakteristike.karakteristicne_rijeci import listaRijeciZaNaivniTest



# Boje
najtamnija_pozadina = 'background-color: #191724;'
tamnija_pozadina = 'background-color: #1F1D2E;'
tamna_pozadina = 'background-color: #26233A;'
iris_pozadina = 'background-color: #C4A7E7;'
svijetli_tekst = 'color: #E0DEF4;'
tamni_tekst = 'color: #191724;'
roza_boja = '#EB6F92'

# Obrubi
bez_obruba = 'border: none;'
obrub = 'border: 1px solid ' + roza_boja + ';'



# Korisničko sučelje
class Sucelje(QMainWindow):



    # Stvori korisničko sučelje
    def __init__(self):
        super().__init__()

        self.setWindowTitle('A10A')

        #podijeli ekran na dva dijela
        lijevo_desno = QSplitter(Qt.Horizontal)
        lijevo_desno.setStyleSheet(najtamnija_pozadina)

        #LIJEVI DIO - unos teksta
        lijevi_dio = self.lijeviDio()

        #DESNI DIO - rezultati
        desni_dio = self.desniDio()

        #dodaj dijelove
        lijevo_desno.addWidget(lijevi_dio)
        lijevo_desno.addWidget(desni_dio)

        lijevo_desno.setSizes([500, 500])

        self.setCentralWidget(lijevo_desno)

        self.showMaximized()


    
    # Detektiraj (glavna funkcija gumba)
    def detektiraj(self):

        #promijeni kursor u pjescani sat
        QApplication.setOverrideCursor(Qt.WaitCursor)

        #ocisti stare rezultate
        if(self.rezultati.layout() != None):
            QWidget().setLayout(self.rezultati.layout())

        #provjeri je li tekst prazan
        if(self.tekst.toPlainText() == ''):
            return
        
        #provjeri je li tekst ili putanja
        putanja = self.putanja.isChecked()
        
        #ako je naivni test pao, prekini s analizom
        if(not self.naivniTest(putanja)):
            #vrati kursor iz pjescanog sata
            QApplication.restoreOverrideCursor()
            return

        #spremi tekst u bazu podataka
        tekst_id = self.spremiTekst()
        
        #izvrsi analizu i prikazi rezultate
        self.izvrsiAnalizu(tekst_id)

        #ako je tekst, a ne putanja, podcrtaj sve karakteristicne rijeci u tekstu
        if(not putanja):
            self.podcrtajKarakteristicneRijeci(tekst_id, putanja)

        #vrati kursor iz pjescanog sata
        QApplication.restoreOverrideCursor()



    # Pripremi lijevi dio
    def lijeviDio(self):
        
        lijevi_dio = QWidget()
        lijevi_raspored = QVBoxLayout()

        #naslov seminara
        self.naslov = self.dodajLabeluIWidget('Naslov: ', QLineEdit(), lijevi_raspored)

        #kvacica je li seminar generiran
        self.generirano = self.dodajLabeluIWidget('Generirano: ', QCheckBox(),
                                                  lijevi_raspored)
        
        #dodatne informacije za generirane seminare
        gen_dio = QWidget()
        gen_raspored = QVBoxLayout()

        #koliko je puta seminar generiran
        self.generirano_puta = self.dodajLabeluIWidget('Generirano puta: ', QSpinBox(), 
                                                       gen_raspored)
        
        #koji je model koristen u generiranju
        modeli = QComboBox()
        modeli.addItems([Modeli.CHAT_GPT.naziv, 
                         Modeli.CLAUDE.naziv,
                         Modeli.GEMINI.naziv])
        self.model = self.dodajLabeluIWidget('Model: ', modeli, gen_raspored)
        
        #koji je upit koristen u generiranju
        self.upit = self.dodajLabeluIWidget('Upit: ', QLineEdit(), gen_raspored)

        #sakrij dodatne informacije i prikazi ih kada se oznaci kvacica generirana 
        gen_dio.setLayout(gen_raspored)
        gen_dio.hide()
        lijevi_raspored.addWidget(gen_dio)
        self.generirano.toggled.connect(gen_dio.setVisible)

        #gumbi za lijepljenje i brisanje u prostor za tekst
        gumbi_raspored = QHBoxLayout()
        gumb_zalijepi = self.dodajGumb('Zalijepi', gumbi_raspored)
        gumb_zalijepi.clicked.connect(self.zalijepi)
        gumb_izbrisi = self.dodajGumb('Izbriši', gumbi_raspored)
        gumb_izbrisi.clicked.connect(self.izbrisi)
        lijevi_raspored.addLayout(gumbi_raspored)

        #prostor za tekst ili putanju do teksta
        self.tekst = QTextEdit(self)
        self.tekst.setPlaceholderText('Upiši tekst ili putanju')
        self.tekst.setStyleSheet(tamnija_pozadina + svijetli_tekst + bez_obruba)
        self.tekst.setFont((QFont('Arial', 12)))
        lijevi_raspored.addWidget(self.tekst)

        #oznaci ako je to putanja a ne tekst
        self.putanja = self.dodajLabeluIWidget('Putanja?', QCheckBox(), lijevi_raspored)

        #gumb za pokretanje detekcije
        gumb_detektiraj = self.dodajGumb('Detektiraj', lijevi_raspored)
        gumb_detektiraj.clicked.connect(self.detektiraj)

        #postavi gotovi raspored u lijevi dio ekrana
        lijevi_dio.setLayout(lijevi_raspored)

        return lijevi_dio


    # Pripremi desni dio
    def desniDio(self):

        desni_dio = QWidget()
        desni_raspored = QVBoxLayout()

        #prostor za rezultate
        self.rezultati = QFrame()
        self.rezultati.setStyleSheet(tamnija_pozadina + svijetli_tekst + bez_obruba)
        self.rezultati.setFont((QFont('Arial', 12)))
        desni_raspored.addWidget(self.rezultati)

        #postavi gotovi raspored u desni dio ekrana
        desni_dio.setLayout(desni_raspored)

        return desni_dio
    


    # Naivni test koji provjerava je li ostao direktan odgovor na upit
    def naivniTest(self, putanja):

        #dohvati primjere direktnih odgovora
        odgovori = listaRijeciZaNaivniTest()

        for odgovor in odgovori:

            c, povlaka = self.kursorIPovlaka()
            
            #pokusaj pronaci primjer u tekstu
            c.movePosition(QTextCursor.Start)
            c = self.tekst.document().find(odgovor, c, QTextDocument.FindCaseSensitively)

            #ako postoji rijec, podcrtaj ju i napisi poruku
            if(c.hasSelection()):
                self.naivniTestPoruka(odgovor)
                if(not putanja):
                    c.mergeCharFormat(povlaka)
                
                return False
        return True
    
    
    # Spremi tekst u bazu podatka i vrati tekst_id
    def spremiTekst(self):

        #izvadi podatke iz oznaka
        naslov = self.naslov.text()
        generirano = self.generirano.isChecked()
        generirano_puta = self.generirano_puta.value()
        model = self.model.currentText()
        upit = self.upit.text()
        tekst_ili_putanja = self.tekst.toPlainText()
        putanja = self.putanja.isChecked()

        #spremi tekst i dohvati dohvati tekst_id
        spremiTekstIzPodatakaSucelja(naslov, generirano, generirano_puta, 
                                     model, upit, tekst_ili_putanja, putanja)
        tekst_id = zadnjiTekstId()

        return tekst_id
        
    
    # Izvrši analizu i prikaži rezultate
    def izvrsiAnalizu(self, tekst_id):
        
        #izracunaj karakteristike, napravi analizu i dohvati rezultate
        rezultati = analizirajTekst(tekst_id)

        #raspored za sve vrijednosti rezultata
        sve = QVBoxLayout()

        #prosjek
        self.dodajRezultat(rezultati['prosjek'], 'Ukupno: ', sve)

        #modeli
        modeli = QHBoxLayout()
        for model in list(Modeli)[1:]:
            self.dodajRezultat(rezultati['modeli'][model.model_id - 1], 
                               model.naziv + ': ', modeli)
        sve.addLayout(modeli)

        #kategorije
        kategorije = QHBoxLayout()
        for kategorija in Kategorije:
            self.dodajRezultat(rezultati['kategorije'][kategorija.kategorija_id - 1], 
                               kategorija.naziv + ': ', kategorije)
        sve.addLayout(kategorije)

        #karakteristike
        karakteristike = QVBoxLayout()
        for karakteristika in KarakteristikeFunkcije:
            self.dodajRezultat(rezultati[karakteristika.karakteristika_id], 
                               karakteristika.naziv + ': ', karakteristike)
        sve.addLayout(karakteristike)

        #prikazi sve rezultate
        self.rezultati.setLayout(sve)


    # Podcrtaj karakteristične riječi i sintagme u tekstu
    def podcrtajKarakteristicneRijeci(self, tekst_id, putanja):

        #dohvati listu karakteristicnih rijeci koje se pojavljuju u tekstu
        rijec_i = listaKarakteristicnihRijeci(tekst_id)

        c, povlaka = self.kursorIPovlaka()

        #idi kroz karakteristicne rijeci
        for rijec in rijec_i:
                
            #postavi kursor na pocetak
            c.movePosition(QTextCursor.Start)

            #idi kroz sva pojavljivanja te rijeci i pocrtaj ih
            while(True):
                c = self.tekst.document().find(rijec, c, QTextDocument.FindWholeWords)
                if(c.isNull()):
                    break
                c.mergeCharFormat(povlaka)



    # Zalijepi tekst iz međuspremnika u prostor za tekst
    def zalijepi(self):
        meduspremnik_tekst = QApplication.clipboard().text()
        self.tekst.setText(meduspremnik_tekst)

    
    # Izbriši tekst iz prostora za tekst
    def izbrisi(self):
        self.tekst.clear()
        


    # Dodaj labelu i widget u određenom stilu u veći raspored
    def dodajLabeluIWidget(self, ime_labele, tip_widgeta, veci_raspored):
        manji_raspored = QHBoxLayout()
        labela = QLabel(ime_labele)
        labela.setFont((QFont('Arial', 12)))
        labela.setStyleSheet(svijetli_tekst)

        widget = tip_widgeta
        if(isinstance(tip_widgeta, QCheckBox)):
            widget.setStyleSheet(svijetli_tekst + bez_obruba)
        else:
            widget.setStyleSheet(tamna_pozadina + svijetli_tekst + bez_obruba)
        widget.setFont((QFont('Arial', 12)))

        manji_raspored.addWidget(labela)
        manji_raspored.addWidget(widget)
        veci_raspored.addLayout(manji_raspored)
        return widget
    

    # Dodaj gumb neki raspored
    def dodajGumb(self, ime_gumba, raspored):
        gumb = QPushButton(ime_gumba, self)
        gumb.setStyleSheet(iris_pozadina + tamni_tekst)
        gumb.setFont((QFont('Arial', 12)))
        raspored.addWidget(gumb)
        return gumb
    

    # Dodaj rezultat u veći raspored
    def dodajRezultat(self, rezultat, ime, veci_raspored, prag=0.5):
        okvir = QFrame()
        okvir_raspored = QHBoxLayout()
        okvir_raspored.setContentsMargins(0, 0, 0, 0)
        
        if(rezultat <= prag):
            okvir.setStyleSheet(tamna_pozadina)
        else:
            okvir.setStyleSheet(tamna_pozadina + obrub)
        
        labela = QLabel(ime + str(round(rezultat, 3)))
        labela.setFont((QFont('Arial', 12)))
        labela.setStyleSheet(svijetli_tekst)
        labela.setAlignment(Qt.AlignCenter)
        okvir_raspored.addWidget(labela)
        okvir.setLayout(okvir_raspored)
        veci_raspored.addWidget(okvir)


    # Stvori kursor i povlaku
    def kursorIPovlaka(self):

        #stvori povlaku
        povlaka = QTextCharFormat()
        povlaka.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        povlaka.setUnderlineColor(QColor(roza_boja))

        #stvori kursor
        c = self.tekst.textCursor()

        return c, povlaka
    

    # Prikaži poruku za pali naivan test
    def naivniTestPoruka(self, rijec):
        veci_raspored = QVBoxLayout()
        okvir = QFrame()
        okvir_raspored = QHBoxLayout()
        okvir_raspored.setContentsMargins(0, 0, 0, 0)
        okvir.setStyleSheet(tamna_pozadina + obrub)
        tekst = QLabel()
        tekst.setText('Tekst sadrži direktan odgovor na upit\n'
                      + 'i obraćanje korisniku:'
                      + '\n' + rijec)
        tekst.setFont((QFont('Arial', 12)))
        tekst.setStyleSheet(svijetli_tekst)
        tekst.setAlignment(Qt.AlignCenter)
        okvir_raspored.addWidget(tekst)
        okvir.setLayout(okvir_raspored)
        veci_raspored.addWidget(okvir)
        self.rezultati.setLayout(veci_raspored)
