"""
Egyszerű ping-pong játék
"""
import tkinter as tk #Rajzolási eszkoz beemelése a kódba 0,0 a bal felső sarok
import random

#LÉPÉSEK
#Ablak létrehozása
#jatek ciklus létrehozása - FPS fogalma - számol, töröl, kirajzol
#Labda változó létrehozása
#Labda kirajzolása
#Labda mozgatása
#Labda pattanása falakról
#játékosok létrehozása
#játékosok kirajzolása
#játékosok mozgatása - eseménykezelés - több billentyűzet - falba ütjözés kezelése
#labda ütése
#pontszám - ha labda oldalfalhoz pattan - új labdamenet

#######################
## GLOBÁLIS VÁLTOZÓK ##
#######################
ablakMagassag = 600
ablakSzelesseg = 1000
meret=10

#kukac={"szin":"green", "vx":-meret, "vy":0, "lepes":meret, "hossz":2, "vastagsag":meret, "test":[[500,300],[480,300]]}
kukac={"szin":"green", "vx":-meret, "vy":0, "lepes":meret, "hossz":1, "vastagsag":meret, "test":[[500,300]]}
alma={"x":100, "y":300, "latszik":0, "pont":1, "szin":"red", "meret":meret}

vege = False

#################################
## Saját függvények, eljárások ##
#################################
#abszolut érték függvény
def abs(arg):
    if arg<0 : return -arg
    return arg


def billentyuMegnyomas(billentyu):
    global kukac, vege
    
    if vege:
        kezdes()
        return

    if billentyu.keycode==111: #nyil fel kódja 111
        if kukac["vy"]!=kukac["lepes"]: #ne tudjon magába fordulni
            kukac["vx"]=0
            kukac["vy"]=-kukac["lepes"]

    if billentyu.keycode==116: #nyil le kódja 116
        if kukac["vy"]!=-kukac["lepes"]:
            kukac["vx"]=0
            kukac["vy"]=kukac["lepes"]

    if billentyu.keycode==113: #nyil bal kódja 113
        if kukac["vx"]!=kukac["lepes"]:
            kukac["vx"]=-kukac["lepes"]
            kukac["vy"]=0

    if billentyu.keycode==114: #nyil jobb kódja 114
        if kukac["vx"]!=-kukac["lepes"]:
            kukac["vx"]=kukac["lepes"]
            kukac["vy"]=0
        
    #print(billentyu.keycode)


def utkozes():
    global kukac, ablakMagassag, ablakSzelesseg, meret
    #fej koordináta
    x = kukac["test"][0][0]
    y = kukac["test"][0][1]
    #pálya széle
    if x<meret/2: return True
    if y<meret/2: return True
    if x>ablakSzelesseg-meret/2: return True
    if y>ablakMagassag-meret/2: return True

    #önmaga
    test=kukac["test"]
    if kukac["hossz"]>1:
        for i in range(1,kukac["hossz"]): #ütközik. e a fej a többi cellával
            if abs(test[i][0] - x)<meret and abs(test[i][1] - y)<meret: return True

    return False    
    


def almaElkapas():
    global kukac, alma, ablakMagassag, ablakSzelesseg
    test=kukac["test"]
    
    #kukac feje (test 0. eleme) és az alma távolságának vizsgálata
    if abs(test[0][0]-alma["x"]) < alma["meret"] and abs(test[0][1]-alma["y"]) < alma["meret"]:
        #nő a kukac
        test.append([test[-1][0],test[-1][1]])
        kukac["hossz"]+=1
        #alma új helyre kerül
        alma["x"]=20+random.randint(0,ablakSzelesseg/20-2)*20
        alma["y"]=20+random.randint(0,ablakMagassag/20-2)*20
        return True    
    
    return False

def kezdes():
    global kukac, alma, vege
    kukac={"szin":"green", "vx":-meret, "vy":0, "lepes":meret, "hossz":1, "vastagsag":meret, "test":[[500,300]]}
    alma={"x":100, "y":300, "latszik":0, "pont":1, "szin":"red", "meret":meret}
    vege = False
    jatek()



def jatek():
    #globális változók
    global c, alma, kukac, vege

    if vege:
        c.create_text(500, 300, text="VÉGE", fill="white", font=('Helvetica 35 bold'))
        #sc.after(50, jatek)#jatek eljárás újbóli meghívása 30ms múlva
        return

    test=kukac["test"]

    #mozgás
    for i in range(kukac["hossz"]-1, -1, -1): #háturól kell kezdeni a ciklust
        if i==0: #fejet tegye az új pozícióba
            test[i][0]=test[i][0]+kukac["vx"]
            test[i][1]=test[i][1]+kukac["vy"]
        else: #minden más az elötte lévő pozícióba menjen
            test[i][0]=test[i-1][0]
            test[i][1]=test[i-1][1]

    if utkozes():
        vege=True

    almaElkapas()

    #[KIRAJZOLÁS]
    c.delete('all') #korábbi tartalom törlése, új képkocka rajzolás megkezdéséhez
    
    #Szöveg
    c.create_text(500, 50, text=str( kukac["hossz"]-1), fill="yellow", font=('Helvetica 35 bold'))

    #alma kirajzolasa
    c.create_rectangle(alma["x"]-alma["meret"]/2,
                       alma["y"]-alma["meret"]/2,
                       alma["x"]+alma["meret"]/2,
                       alma["y"]+alma["meret"]/2,
                       fill=alma["szin"])

    #kukac kirajzolás
    for i in range(0,kukac["hossz"]):
        if i==0:
            c.create_rectangle(test[i][0]-kukac["vastagsag"]/2,
                       test[i][1]-kukac["vastagsag"]/2,
                       test[i][0]+kukac["vastagsag"]/2,
                       test[i][1]+kukac["vastagsag"]/2,
                       fill=kukac["szin"],
                       outline=kukac["szin"])
        else:
            c.create_rectangle(test[i][0]-kukac["vastagsag"]/2,
                       test[i][1]-kukac["vastagsag"]/2,
                       test[i][0]+kukac["vastagsag"]/2,
                       test[i][1]+kukac["vastagsag"]/2,
                       outline=kukac["szin"])
                       #fill=kukac["szin"])


    #A háttérben rajzolt tartalom megjelenítése
    sc.update() 
    
    sc.after(50, jatek)#jatek eljárás újbóli meghívása 30ms múlva




#############################
## PROGRAM BELÉPÉSI PONTJA ##
#############################
#Itt indul a program
if __name__ == "__main__":    
    sc = tk.Tk()# Grafikus ablak létrehozása
    sc.title("Kigyo")#ablak címe    
    sc.geometry("1000x600")#ablak mérete
    sc.resizable(False, False)#nem lehet átméretezni

    #fekete rajzvászon létrehozása
    c=tk.Canvas(sc, bg="black")
    c.pack(fill="both", expand=True)#

    sc.bind('<KeyPress>', billentyuMegnyomas) #Egérmozgást kezelő regisztrálása
    sc.update()#tartalom frissítése        
    print("Kukac mozgatása nyilakkal")
    kezdes() #játék indítása)    
    sc.mainloop() # Minden Python Tk programot így kell befejezni