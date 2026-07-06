import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



# Nacrtaj box graf vrijednosti određene karakteristike prema modelima
def nacrtajGrafKarakteristike(karakteristika_id):

    np.random.seed(10)

    #procitaj sadrzaj dokumenta
    putanja = 'grafovi/podatci/' + str(karakteristika_id) + '.csv'
    redci = open(putanja, encoding='utf-8-sig').readlines()

    #postavi celije u matricu
    matrica = []
    for red in redci:
        celije = red.strip().split(',')
        matrica.append(celije)

    #postavi podatke za graf u matricu
    skupovi = []
    df = pd.DataFrame(matrica)

    labele = [df[0][0], df[1][0], df[2][0], df[3][0]]

    for stupac in df.columns:
        col = pd.to_numeric(df[stupac][1:], errors='coerce')
        skupovi.append(col.dropna().values)

    #pripremi graf
    fig = plt.figure()
    ax = fig.add_subplot()

    graf = ax.boxplot(skupovi, patch_artist=True)

    #dodaj boje
    boje = ["#312D4D", "#97193D", "#F03066", "#EB6F92"]
    for box, color in zip(graf['boxes'], boje):
        box.set_facecolor(color)
    
    #dodaj labele
    ax.set_xticklabels(labele)

    plt.show()



# Nacrtaj graf točnosti po pragovima konačne odluke
def nacrtajGrafTocnostiPragova():

    np.random.seed(10)

    #procitaj sadrzaj dokumenta
    putanja = 'grafovi/podatci/prag.csv'
    redci = open(putanja, encoding='utf-8-sig').readlines()

    #postavi celije u matricu
    matrica = []
    for red in redci:
        celije = red.strip().split(',')
        matrica.append(celije)

    #postavi podatke za graf u matricu
    df = pd.DataFrame(matrica)

    #x-os
    x = pd.to_numeric(df[0][1:])
    plt.xlabel(df[0][0])
    plt.ylabel(df[1][0])

    #nacrtaj graf
    plt.plot(x, pd.to_numeric(df[1][1:]), color="#A169E6")

    plt.grid()
    plt.show()



# Nacrtaj graf točnosti za modele po pragovima konačne odluke
def nacrtajGrafTocnostiModelaPragova():

    np.random.seed(10)

    #procitaj sadrzaj dokumenta
    putanja = 'grafovi/podatci/prag.csv'
    redci = open(putanja, encoding='utf-8-sig').readlines()

    #postavi celije u matricu
    matrica = []
    for red in redci:
        celije = red.strip().split(',')
        matrica.append(celije)

    #postavi podatke za graf u matricu
    df = pd.DataFrame(matrica)

    #x-os
    x = pd.to_numeric(df[0][1:])
    plt.xlabel(df[0][0])

    #dodaj boje
    boje = ["#4C3EA7", "#97193D", "#F03066", "#EB6F92"]

    #nacrtaj grafove
    for i in range(2, 6):
        plt.plot(x, pd.to_numeric(df[i][1:]), label=df[i][0], color=boje[i - 2])

    plt.grid()
    plt.legend()
    plt.show()
