"""
Az ismert snake játék
"""
import tkinter as tk #Rajzolási eszkoz beemelése a kódba 0,0 a bal felső sarok
import random

#LÉPÉSEK
#List és Dictionary fogalma használata. Ciklusban lista minden elemét lekérdezni, változtatni
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

kukac={}
alma={}

vege = False

#################################
## Saját függvények, eljárások ##
#################################
#abszolut érték függvény
def abs(arg):
    if arg<0 : return -arg
    return arg

#keycode más Linuxon, mint Windowson. A hordozhatóság érdekében a keysym (szimbolum) használatos.
def billentyuMegnyomas(billentyu):
    global kukac, vege
    
    print(billentyu.keysym," : ", billentyu.keycode)

    if vege:
        kezdes()
        return

    if billentyu.keysym=="Up": #nyil fel kódja 111
        if kukac["vy"]!=kukac["lepes"]: #ne tudjon magába fordulni
            kukac["vx"]=0
            kukac["vy"]=-kukac["lepes"]

    if billentyu.keysym=="Down": #nyil le kódja 116
        if kukac["vy"]!=-kukac["lepes"]:
            kukac["vx"]=0
            kukac["vy"]=kukac["lepes"]

    if billentyu.keysym=="Left": #nyil bal kódja 113
        if kukac["vx"]!=kukac["lepes"]:
            kukac["vx"]=-kukac["lepes"]
            kukac["vy"]=0

    if billentyu.keysym=="Right": #nyil jobb kódja 114
        if kukac["vx"]!=-kukac["lepes"]:
            kukac["vx"]=kukac["lepes"]
            kukac["vy"]=0
        

def utkozes():
    global kukac, ablakMagassag, ablakSzelesseg, meret
    #fej koordináta
    x = kukac["test"][0][0] #0. cella 0. eleme
    y = kukac["test"][0][1] #0. cella 1. eleme
    #pálya szélével ütközik?    
    if x<meret/2: return True #bal széle
    if y<meret/2: return True #teteje
    
    if x>ablakSzelesseg-meret/2: return True #jobb széle
    if y>ablakMagassag-meret/2: return True #alja

    #önmaga
    test=kukac["test"]
    if kukac["hossz"]>4: #akkor kell csak önmaga ütközést vizsgálni, ha képes is rá
        for i in range(1,kukac["hossz"]): #ütközik-e a fej másik cellával
            if abs(test[i][0] - x)<meret and abs(test[i][1] - y)<meret: return True

    #ha nem talált ütközést
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
    alma={"x":250, "y":300, "latszik":0, "pont":1, "szin":"red", "meret":meret}
    vege = False
    jatek()



def jatek():
    #globális változók
    global c, alma, kukac, vege

    if vege:
        c.create_text(500, 300, text="VÉGE", fill="white", font=('Helvetica 35 bold'))        
        return

    #mozgás
    test=kukac["test"] #csak a testtel egyszerübb
    for i in range(kukac["hossz"]-1, -1, -1): #háturól kell kezdeni a ciklust
        if i==0: #fejet tegye az új pozícióba
            test[i][0]=test[i][0]+kukac["vx"]
            test[i][1]=test[i][1]+kukac["vy"]
        else: #hátulról előre haladva minden az elötte lévő pozícióba menjen
            test[i][0]=test[i-1][0]
            test[i][1]=test[i-1][1]

    #van-e ütközés?
    if utkozes():
        vege=True

    #van-e alma elkapás?
    almaElkapas()

    #[KIRAJZOLÁS]
    c.delete('all') #korábbi tartalom törlése, új képkocka rajzolás megkezdéséhez
    
    #Szöveg - elsőként, hogy ne takarja az almat, vagy a kukacot
    c.create_text(500, 50, text=str( kukac["hossz"]-1), fill="yellow", font=('Helvetica 35 bold'))

    #alma kirajzolasa, az eltárolt koordináta az alma közepe
    c.create_rectangle(alma["x"]-alma["meret"]/2,
                       alma["y"]-alma["meret"]/2,
                       alma["x"]+alma["meret"]/2,
                       alma["y"]+alma["meret"]/2,
                       fill=alma["szin"])

    #kukac kirajzolás, az eltárolt koordináták a cellák közepe
    for i in range(0,kukac["hossz"]):
        if i==0: #fej rajzolása eltér, teli cella
            c.create_rectangle(test[i][0]-kukac["vastagsag"]/2,
                       test[i][1]-kukac["vastagsag"]/2,
                       test[i][0]+kukac["vastagsag"]/2,
                       test[i][1]+kukac["vastagsag"]/2,
                       fill=kukac["szin"],
                       outline=kukac["szin"])
        else: #csak cella keret
            c.create_rectangle(test[i][0]-kukac["vastagsag"]/2,
                       test[i][1]-kukac["vastagsag"]/2,
                       test[i][0]+kukac["vastagsag"]/2,
                       test[i][1]+kukac["vastagsag"]/2,
                       #fill=kukac["szin"],
                       outline=kukac["szin"])
                       


    #A háttérben rajzolt tartalom megjelenítése
    sc.update() 

    #jatek eljárás újbóli meghívása 50ms múlva - gyorsítás / lassítás
    sc.after(50, jatek)




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
