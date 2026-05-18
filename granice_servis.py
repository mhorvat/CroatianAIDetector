# SEMANTIČKE

# Udio jedinstvenih riječi
def udioJedinstvenihTokena(tekst):
    return len(set(tekst.tokeni)) / tekst.broj_tokena()

def udioJedinstvenihRijeci(tekst):
    return len(set(tekst.rijeci_norm)) / tekst.broj_rijeci()


# Udio brojeva
def udioBrojeva(tekst):
    return sum(1 for t in tekst.tokeni if t.isdigit()) / tekst.broj_tokena()
