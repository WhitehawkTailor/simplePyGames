

# https://www.youtube.com/watch?v=w8yWXqWQYmU

"""
Kézzel írott 28x28pixelben tárolt számjegyeket felismerő neurális háló.

A hálónak 784 (28x28=784) bemeneti neuronja van (A0).
A rejtett rétege 10 neuronból áll (A1).
A kimeneti rétege 10 neuronból áll (A2).
A második és harmadik réteg neuronjai minden a közvetlen megelöző rétegben lévő neuronnal össze van kötve.
Az összekötést egy súly jelenti, ami megmondja, hogy a hatás mennyire terjed át a neuronra.


Egy csv fájlban vannak a kézzel írot számjegyek 28x28pixeles mátrixokban.
A CSV fájl egy sora egy számjegyet tartalmaz.
Első oszlop a kérdéses számjegy.
A sor többi eleme a 28x28-as pixel mátrix sorait tartalmazza egymás után.
Egy pixel egy egy byte-os szám jelképez.
Ez szürke skálán adja meg egy pixel szín értékét (0 fekete, 255 fehér).

A CSV adatot át kell alakítani.
Elöször is a teljes listát félbe kell venni.
Első fele lesz a tanuló adat. A második fele lesz a teszt adat.

Az első oszlop a végeredményt tartalmazza.

Minden sor egy szám adatait tartalmazza. A 28x28 terület sorai egymás után vannak felsorolva.
Ebből az első elemeket (ami a szám megnevezése) egy külön listába kell tenni.
A megmaradt adatok a 28x28 pixel mátrix adatai.
Ezt kell egy egydimenziós tömbbé alakítani, ami egy rajzolathoz 28x28=784 értéket tartalmaz.
Ezeket kell egy listába betenni. Így kész a képadatokat tartalmazó adat.

Ennek a tömbnek az elemei egy pixel képet tartalmazó tömb.
Feldolgozáskor az elemeit adjuk rá a neurális háló bemeneti elemeire.
A bemeneti réteg neuronjainak jelölése A0
Ebből a középső rejtett réteg neuronjára adott értéket kell kiszámolni, ami a Z1.
A Z1 érték minden neuronnak egy hozzá kötött neuron értéke (A0) és az összekötés sullya (W1),
valamint egy tetszőleges eltolás (b1) adja meg.
Z1 = A0 x W1 + b1
Z1 egy 10 elemű tömb. Ebből az m db számú minta esetén lesz m tömb.
A W1 784 elemet köt össze 10 elemmel, ezért 10 x 784 eleme van
AZ A0-ban 784 bemeneti érték van és m db mintát kell átszámolni.

A második rétegben lévő neuron értékét még egy neuronra jellemző átviteli fügyvény is befolyásolja.
Így a második réteg neuron értékek (A1) az alábbi módon kell számolni:
A1 = f1(Z1)   ahol az f1() függvén az átviteli fügvény, ami Z1 alapján ad értéket az A1 réteg elemeinek.
Az átviteli fuggvény (ReLu):
f1() = (x>0 ? x : 0)   A föggvény alakja:  _/
A1 = f1(Z1) = f1(A0 x W1 + b1)

A következő réteggel ugyan ezt kell végig vinni, de más az átviteli függvény.
Z2 = A1 x W2 + b2
A2 = f2(Z2) = f2(A1 x W2 + b2)

Az f2() átviteli fügvény feladata, hogy a kimeneti értékeket 0-1 közé hozza.
Így a kimeneti érték az adott neuronhoz rendelt számjegy valószínűségét (probability) fogja jelenteni.
Az f2() neve softmax ( e^Zi ) / SUM.K-j=1( e^Zj)

Kell két folyamat:
1)Az egyik odafelé kiszámolja egy bemenet alapján a kimenetet.
2)A másik a bemenetre adott kimeneti válasz és a helyes válasz ismeretében visszafelé terjeztve a hibát a kimenettől indulva a bemenet felé állít a paramétereken.
A súlyok és az eltolás mértékét kell változtatni.
Gyakorlatilag ezek az értékek reprezentálják a tudást a hálóban.
Ez az eljárás a back propagation, vagyis a hiby visszafelé terjesztése.
Ez megerősiti egy adott minta esetén a jó választ elősegítő kapcsolatokat és gyengíti a rossz választ eredményezőket.

Backward propagation - visszafelé terjesztés
Hiba a kimeneti rétegen a kimeneti érték (A2 tömb) és a jó eredmény (Y tömb) különbsége.
Pl A2[0.1, 0.2, 0.05, 0.9 ....]
dZ2 = A2 - Y   a második réteg hibája 
dZ2 egy 10 elemű tömb
A2 egy 10 elemű tömb
Y is 10 elemű tömb

 





pl y=2, akkor az eredmény vekrot Y=[0,0,1,0,0,0,0,0,0,0], ha a 2 a helyes eredmény. Az 1 a 2-nek megfelelő kimeneten van.



"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


#adatok beolvasása
data = pd.read_csv('train.csv') #train.zip-ből ki kell csomagolni
data = np.array(data) #tömböt készít belőle, de kihagyja az első sort, ami a neveké
m, n = data.shape   #m sorok (ennyi minta van -1 title sor) és n oszlopok, beleértve az oszlop nevek sorát is
np.random.shuffle(data)  #megkeveri a sorokat, hogy ne sorrendbe legyenek a számok

data_dev = data[0:1000].T #a data dev az első 1000 sor de elforgatva =-ből || lesz.
Y_dev = data_dev[0] #ebben vannak a számjegek "neve"
X_dev = data_dev[1:n] #ebben a számjegyek 28x28 adatai (kihagyja a labelt, ami a korábbi oszlopnevek)
X_dev = X_dev / 255.  #Az értékek 0és 1 közé essenek

data_train = data[1000:m].T #A következő 1000 sor lesz a tanító data
Y_train = data_train[0] #ebben vannak a számjegek "neve"
X_train = data_train[1:n] #ebben a számjegyek 28x28 adatai (kihagyja a labelt, ami a korábbi oszlopnevek)
X_train = X_train / 255. #Az értékek 0és 1 közé essenek



def init_params():
    #randn() 0-1 közötti véletlen számokat ad vissza
    ##értékek suly és bias -0.5 és 0.5 közé essenek, ezért a -0.5
    W1 = np.random.rand(10, 784)-0.5  #10 x 784 mátrixot tölt fel véletlen számokkal .rand(10, 784)  0-1 között   randn -0,5 és 0.5 között
    b1 = np.random.rand(10,1)-0.5 #10 x 1 mátrixot tölt fel véletlen számokkal
    W2 = np.random.rand(10, 10)-0.5  #10 x 10 mátrixot tölt fel véletlen számokkal. -0,5 nem kell
    b2 = np.random.rand(10,1)-0.5 #10 x 1 mátrixot tölt fel véletlen számokkal
    return W1, b1, W2, b2

#Megvalósítja a _/ függvényt
def ReLU(Z):
    return np.maximum(Z, 0) # két vektor elemeiből páronként a nagyobbat adja vissza


#Normalizálja a vektort, hogy az értékek 0-1 közé essenek, de megtartsák egymáshoz képesti arányukat.
def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A


#Kiszámolja a bemenetre adott értékekhez tartozó kimenetet
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1 #.dot operátor az mátrix szorzás
    A1 = ReLU(Z1)
    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


def deriv_ReLu(Z):
    return Z > 0



def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max()+1 ))
    one_hot_Y[np.arange(Y.size),Y] = 1
    return one_hot_Y.T


#Visszafelé haladva az elvárt kimeneti értékhez igazítja a súlyokat és az eltolás mértékét.
#Cél, hogy a haló belső paraméterei úgy változzanak, hogy a bemenetre adott válasz a kimeneten közelítsen az elvárthoz
def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    m=Y.size
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    dW2 = 1/m * dZ2.dot(A1.T)
    db2 = 1/m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * deriv_ReLu(Z1)
    dW1 = 1/m *dZ1.dot(X.T)
    db1 = 1/m * np.sum(dZ1)
    return dW1, db1, dW2, db2


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2


def get_predictions(A2):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size


#Make NeuronNetwork training run
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)
            print(get_accuracy(predictions, Y))
    return W1, b1, W2, b2


#Kérdezés
def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
    label = Y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)
    
    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')
    plt.show()




#Program belépési pontja
#Tanítás
W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.10, 500)
a=input("Tanitás vége. Nyomj Entert")
test_prediction(0, W1, b1, W2, b2)
a=input("Nyomj Entert")
test_prediction(1, W1, b1, W2, b2)
a=input("Nyomj Entert")
test_prediction(2, W1, b1, W2, b2)
a=input("Nyomj Entert")
test_prediction(3, W1, b1, W2, b2)
a=input("Vége - Nyomj Entert")

