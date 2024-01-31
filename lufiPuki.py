"""
Egyszerű lufi nyilazós játék
"""
import tkinter as tk #Rajzolási eszkoz beemelése a kódba 0,0 a bal felső sarok
import math #szögek, távolság számításához
import random #véletlen szám generáláshoz

#LÉPÉSEK
#Ablak létrehozása
#jatek ciklus létrehozása - FPS fogalma - számol, töröl, kirajzol
#Lufik változó létrehozása
#Lufik kirajzolása
#Lufik mozgatása
#Ágyu létrehozása
#Ágyu kirajzolása
#Ágyu mozgatása - eseménykezelés - több billentyűzet - falba ütjözés kezelése
#Lövedék létrehozása
#Lövedék mozgatása
#pontszám - ha lövedék lufiba ütközik - lövéskor - Lufi leesik

#######################
## GLOBÁLIS VÁLTOZÓK ##
#######################
pontszam=0
tik=0
tak=0
#ágyu paramétereinek tárolása listában: x,y,irany,hossz
agyu = [500, 570, 180, 30] #adott pontban, függőleges irány, 30 pixel hosszú

#lufik tárolása listában listák. [x,y, meret] - kezdésnek két lufi
lufik = [[100,-20, 20], [600,-30, 30]]
#Repulő lövedékek tárolása listában listák [x, y, irány, méret] - kezdetben nincs repülő lövedék
lovedekek = []
eredmenySzoveg=""

#################################
## Saját függvények, eljárások ##
#################################

#egérmozgás kezelése -  mozgatja az ágyút - ágyú szög számítása az agyu és a kurzor koordinátáiból és arctgn függvénnyel
def egerMozgas(esemeny):    
    agyu[2]=int(round(math.degrees(math.atan2(esemeny.x-agyu[0],esemeny.y-agyu[1]))))
    #print("szog:",agyu[2])
    if agyu[2]<0: agyu[2]=agyu[2]+360
    if agyu[2]>260 : agyu[2]=260
    if agyu[2]<100 : agyu[2]=100

#egérkattintás kezelése - lövés
def egerKattintas(esemeny):
    global pontszam, eredmenySzoveg
    pontszam = pontszam - 1 #minden lövés levon egy pontot
    eredmenySzoveg="pontszam: " + str(pontszam) + "  -1" #lövésenként eggyel csökken a pontszám
    #lövedék létrehozása az ágyu végpontjában az ágyú szögével
    lovedekek.append( [agyu[0]+agyu[3]*math.sin(agyu[2]*math.pi/180),
                            agyu[1]+agyu[3]*math.cos(agyu[2]*math.pi/180), 
                            agyu[2], 
                            8] )

#vonalat rajzoló rutin - szin-nel, kezdőpont x,y, iranyszög és hossz alapján.
def drawLineToDirection(x, y, irany, hossz, szin):    
    #vonal vége koordináták kiszámolása x,y indulópont adott szög és hossz segítségével
    posX=x+hossz*math.sin(irany*math.pi/180)
    posY=y+hossz*math.cos(irany*math.pi/180)
    c.create_line(x, y, posX, posY, fill=szin)#vonal rajzolása

#kiszámítja két pont közötti távolságot - Phitagorasz tétel alapján a koordinátákból
def tavolsag(x1, y1, x2, y2):
    tav=math.sqrt( (x2-x1)**2+(y2-y1)**2  ) # **2 jelentése a négyzeten, sqrt négyzetgyök
    return tav


#A játék fő ciklusa
#kiszámolja a játék elemek értékeinek változását
#és kirajzolja az elemeket, 
#majd időzítve újra futtatja magát
def jatek():
    #globális változók
    global agyu, pontszam, lovedek, lufik, tik, tak, eredmenySzoveg
    tik = tik + 1 #időkezeléshez
    tak = tak + 1 #időkezeléshez

    #szamolas - Lufik
    #Új lufik létrehozása
    if tik==100:
        tik=0
        lufik.append([random.randint(50,950),-50, random.randint(1,3)*20])
        if tak%random.randint(3,7)==0:
            lufik.append([random.randint(50,950),-50, random.randint(1,3)*20])

    #lufik zuhanása
    for lufi in lufik:
        lufi[1] = lufi[1] + 3
        if lufi[1]>600:
            lufik.remove(lufi) #ha kiesik tünjön el a listából
            pontszam = pontszam - 50
            eredmenySzoveg="pontszam: " + str(pontszam) + "  -50"

    #Lövedék számítások
    for lovedek in lovedekek:
        #lövedék haladásának számítása - az irányba eső hosszal arréb kell rakni a lövedéket
        lovedek[0]=lovedek[0]+lovedek[3]*math.sin(lovedek[2]*math.pi/180)
        lovedek[1]=lovedek[1]+lovedek[3]*math.cos(lovedek[2]*math.pi/180)        

        #lovedék és lufi ütközése esetén a lufi is és a lövedék is kerüljön ki a listából - megsemmisülés
        for lufi in lufik:
            if tavolsag(lufi[0], lufi[1], lovedek[0], lovedek[1]) < lufi[2]: #távolság kisebb, mint a lufi sugara
                lovedekek.remove(lovedek)
                lufik.remove(lufi)
                pontszam = pontszam + 5 #találat esetén pontszám növelése
                eredmenySzoveg="pontszam: " + str(pontszam) + "  +5"

        #lövedék és oldalfal ütközése esetén a lövedék kerüljön ki a listából, mintha kiment volna a képről
        #ritkán előfordulhat, hogy a lövedék a lufi ütközés miatt már kikerült a listából de a fal ütközés miatt is ki kell venni
        if lovedek in lovedekek :
                #    x<0                  x>1000          y<0
            if lovedek[0]<0 or lovedek[0]>1000 or lovedek[1]<0 : 
                lovedekek.remove(lovedek)    
            

    #kirajzolás
    c.delete('all') #korábbi tartalom törlése, új képkocka rajzolás megkezdéséhez
    
    #Lufik - a listában tárolt összes kirajzolása
    for lufi in lufik:
        c.create_oval(lufi[0]-lufi[2], lufi[1]-lufi[2], lufi[0]+lufi[2], lufi[1]+lufi[2], fill='red') #kör rajzoláshoz: x-r, x+r, y-r, y+r, fill="blue"
    
    #Lövedékek - a listában tárolt összes kirajzolása
    for lovedek in lovedekek:
        drawLineToDirection(lovedek[0], lovedek[1], lovedek[2], lovedek[3], 'yellow')
    
    #Ágyu kirajzolása     x         y   irányszög   hossz   szín
    drawLineToDirection(agyu[0], agyu[1], agyu[2], agyu[3], 'cyan')    
    #szöveg kiírása
    c.create_text(500, 580, text=eredmenySzoveg, fill="yellow", font=('Helvetica 15 bold'))

    #A háttérben rajzolt tartalom megjelenítése
    sc.update() 
    
    sc.after(30, jatek)#jatek eljárás újbóli meghívása 30ms múlva


#############################
## PROGRAM BELÉPÉSI PONTJA ##
#############################
#Itt indul a program
if __name__ == "__main__":    
    sc = tk.Tk()# Grafikus ablak létrehozása
    sc.title("Lufi Puki")#ablak címe    
    sc.geometry("1000x600")#ablak mérete
    sc.config(cursor="cross") #célkereszt legyen a kurzor
    sc.resizable(False, False)#nem lehet átméretezni
    
    #fekete rajzvászon létrehozása
    c=tk.Canvas(sc, bg="black")
    c.pack(fill="both", expand=True)#
    
    sc.bind('<Motion>', egerMozgas) #Egérmozgást kezelő regisztrálása
    sc.bind('<ButtonPress-1>', egerKattintas) #Egér kattintást kezelő regisztrálása
    sc.update()#tartalom frissítése        

    jatek() #játék indítása
    sc.mainloop() # Minden Python Tk programot így kell befejezni