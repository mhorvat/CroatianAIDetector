import nltk



# Klasa Tekst
class Tekst:
    def __init__(self, tekst):
        self.tokeni = nltk.word_tokenize(tekst)
        self.rijeci = [t for t in self.tokeni if t.isalpha()]
        self.frek = nltk.FreqDist(self.tokeni)
        self.rijeci_norm = [r.lower() for r in self.rijeci]
        self.recenice = nltk.sent_tokenize(tekst)
        
    def broj_tokena(self):
        return len(self.tokeni)
    
    def broj_rijeci(self):
        return len(self.rijeci)
    
    def broj_recenica(self):
        return len(self.recenice)

    def n_grami_frek(self, n=1):
        n_grami = list(nltk.ngrams(self.rijeci_norm, n))
        return nltk.FreqDist(n_grami)
    