"""
Egyszerű ping-pong játék
"""
import tkinter as tk #Rajzolási eszkoz beemelése a kódba 0,0 a bal felső sarok
import math #szögek, távolság számításához

#LÉPÉSEK
#Dictionary fogalma használata
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
labdaSebesség=15
utoSebesseg=10
kezdet = True

jatekosA={"x":20, "y":300, "v":utoSebesseg, "vy":0, "size":90, "pont":0}
jatekosB={"x":980, "y":300, "v":utoSebesseg, "vy":0, "size":90, "pont":0}
labda={"x":500, "y":300, "v":labdaSebesség, "vx":labdaSebesség, "vy":0, "meret":10}


#################################
## Saját függvények, eljárások ##
#################################

def billentyuMegnyomas(billentyu):
    global jatekosA, jatekosB, kezdet
    
    #print(billentyu.keysym," : ", billentyu.keycode)

    if kezdet:
        kezdet = False
        jatek()
        return

    #Q fel
    if billentyu.keysym=="q": #Q(fel) kódja 24
        jatekosA["vy"]=-jatekosA["v"] #a felfelé negatív irányban van
    #A le
    if billentyu.keysym=="a": #A(le) kódja 38
        jatekosA["vy"]=jatekosA["v"] #a lefelé pozitív irányban van

    #nyil fel
    if billentyu.keysym=="Up": #nyil fel kódja 111
        jatekosB["vy"]=-jatekosB["v"] #a felfelé negatív irányban van
    #nyil le
    if billentyu.keysym=="Down": #nyil le kódja 116
        jatekosB["vy"]=jatekosB["v"] #a lefelé pozitív irányban van


def billentyuElengedes(billentyu):
    if billentyu.keysym=="q" or billentyu.keysym=="a": #Q vagy A
        jatekosA["vy"]=0 #álljon meg

    if billentyu.keysym=="Up" or billentyu.keysym=="Down" : #fel vagy le nyil
        jatekosB["vy"]=0 #álljon meg



def labdaMozgatas():
    global labda
    labda["x"]=labda["x"]+labda["vx"]
    labda["y"]=labda["y"]+labda["vy"]



def utes(jatekos):
    global labda
    
    #visszapattanási szög 45 és 135fok között arányos ahoz képest, ahol alabda eltaláta az ütőt
    szog = (labda["y"] - (jatekos["y"]-jatekos["size"]/2)) / jatekos["size"] * 90

    #ki kell számítani a szögből a koordinátát
    #A ütött vx>0, szög 135-45
    if labda["vx"]<0:
        szog=135-szog
    else : #B ütött vx<0, szög 225-315
        szog=225+szog

    labda["vx"]=labda["v"]*math.sin(szog*math.pi/180)
    labda["vy"]=labda["v"]*math.cos(szog*math.pi/180)
    #induljon visszafelé a labda
    labdaMozgatas()



def jatek():
    #globális változók
    global jatekosA, jatekosB, labda, c, ablakMagassag, ablakSzelesseg, kezdet


    if kezdet :
        c.create_text(500, 120, text="Iranyítás  q,a  /  Fel,Le", fill="yellow", font=('Helvetica 30 bold'))
        c.create_text(500, 200, text="új játékhoz nyomj egy gombot", fill="green", font=('Helvetica 35 bold'))
        return

    #[SZÁMOLÁS]
    #ütő mozgatása A
    if jatekosA["vy"]!=0:
        jatekosA["y"]+=jatekosA["vy"]
    #ne menjen ki felül    
    if jatekosA["y"] - jatekosA["size"]/2 < 0 : jatekosA["y"] = jatekosA["size"]/2
    #ne menjen ki alul
    if jatekosA["y"] + jatekosA["size"]/2 > ablakMagassag : jatekosA["y"] = ablakMagassag - jatekosA["size"]/2

    #ütő mozgatása B
    if jatekosB["vy"]!=0:
        jatekosB["y"]+=jatekosB["vy"]
    #ne menjen ki felül    
    if jatekosB["y"] - jatekosB["size"]/2 < 0 : jatekosB["y"] = jatekosB["size"]/2
    #ne menjen ki alul
    if jatekosB["y"] + jatekosB["size"]/2 > ablakMagassag : jatekosB["y"] = ablakMagassag - jatekosB["size"]/2

    #labda mozgatása
    labdaMozgatas()
    
    #ha labda ütőt ér
    #Az A jatekos mögött van a labda de az ütő területét éri el
    if labda["x"] < jatekosA["x"]:
        if labda["y"]>jatekosA["y"]-jatekosA["size"]/2 and labda["y"]<jatekosA["y"]+jatekosA["size"]/2:            
            utes(jatekosA)

    #A B jatekos mögött van a labda de az ütő területét éri el
    if labda["x"] > jatekosB["x"]:
        if labda["y"]>jatekosB["y"]-jatekosB["size"]/2 and labda["y"]<jatekosB["y"]+jatekosB["size"]/2:
            utes(jatekosB)

    #ha labda pálya alsó, felső szélét éri
    if labda["y"]<0 or labda["y"]>ablakMagassag:
        labda["vy"] *= -1 #pattanjon vissza
        labdaMozgatas()

    #ha labda jobb, bal szélét éri - pontszámítás
    if labda["x"]<0 or labda["x"]>ablakSzelesseg:
        #pontszamítás
        if labda["vx"] < 0 :#A-nál ment ki a labda
            jatekosB["pont"]+=1
            labda["vx"]=labda["v"]
        else :        #B-nél ment ki a labda
            jatekosA["pont"]+=1
            labda["vx"]=-labda["v"]

        #új menethez a labda középre kerül és vízszintesen indul
        labda["vy"]=0
        labda["x"]=500
        labda["y"]=300

        

    #[KIRAJZOLÁS]
    c.delete('all') #korábbi tartalom törlése, új képkocka rajzolás megkezdéséhez
    #ütők rajzolása
    c.create_rectangle(jatekosA["x"]-20, jatekosA["y"]-jatekosA["size"]/2, jatekosA["x"], jatekosA["y"]+jatekosA["size"]/2, fill="red")#vonal rajzolása
    c.create_rectangle(jatekosB["x"], jatekosB["y"]-jatekosB["size"]/2, jatekosB["x"]+20, jatekosB["y"]+jatekosB["size"]/2, fill="red")#vonal rajzolása
    #Labda rajzolása
    c.create_rectangle(labda["x"]-labda["meret"]/2,
                       labda["y"]-labda["meret"]/2,
                       labda["x"]+labda["meret"]/2,
                       labda["y"]+labda["meret"]/2,
                       fill="white")

    #Szöveg
    c.create_text(500, 50, text=str( jatekosA["pont"]) + " : " + str(jatekosB["pont"] ), fill="yellow", font=('Helvetica 35 bold'))

    #A háttérben rajzolt tartalom megjelenítése
    sc.update() 
    
    sc.after(30, jatek)#jatek eljárás újbóli meghívása 30ms múlva


#############################
## PROGRAM BELÉPÉSI PONTJA ##
#############################
#Itt indul a program
if __name__ == "__main__":    
    sc = tk.Tk()# Grafikus ablak létrehozása
    sc.title("Pong")#ablak címe    
    sc.geometry("1000x600")#ablak mérete
    sc.resizable(False, False)#nem lehet átméretezni

    #fekete rajzvászon létrehozása
    c=tk.Canvas(sc, bg="black")
    c.pack(fill="both", expand=True)#

    sc.bind('<KeyPress>', billentyuMegnyomas) #Egérmozgást kezelő regisztrálása
    sc.bind('<KeyRelease>', billentyuElengedes) #Egérmozgást kezelő regisztrálása
    sc.update()#tartalom frissítése        
    print("Utok mozgatasa: Q,A és Fel,Le nyilak")
    jatek() #játék indítása
    sc.mainloop() # Minden Python Tk programot így kell befejezni
