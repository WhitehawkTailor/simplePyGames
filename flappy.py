"""
Klasszikus flappy Bird egyszerűsített változata.
Van egy négyzet ami a képernyő bal szélénél található.
Ez alapvetően lezuhan, ha nem nyom meg a játékos egy billentyűt.
Billentyű nyomá hatására felfelé ugrik, majd megint zuhanni kezd (mind amikor csapkod a szárnyával a madár)
A képernyő jobb széléről indulnak el más szinű négyzetek (vagy körök), amik az akadályokat képezik.
A madárnak csapkodva el kell kerülni a jobbról balra haladó akadályokat.

"""


#Rajzolási eszkoz beemelése a kódba
import tkinter as tk #0,0 a bal felső sarok
import math
import random

ablakMagassag = 600
ablakSzelesseg = 1000
pontszam=0
vege=False
kezdet=True

#madár paramétereinek tárolása 
madarDy=-7 #a madar emelkedési, vagy zuhanási ideje (képkocka)
madar = {}
madarHaladas=5

#akadályok koordinátáinak tárolása listában. [x,y, meret]
akadalyok = []
akadalySzam = 30
soronként=3
akadálySorTav=100
akadályDx=-5 #az akadályok sebessége pixel/képkocka


def gombLenyomas(esemeny):   
    global madarDy, madar, kezdet
    
    if kezdet:
        kezdet = False
        jatek()

    if vege:
        #print(esemeny.keysym," : ", esemeny.keycode)
        if esemeny.keysym=="Return" : kezdes()
        return

    #reppenés bármilyen gomb lenyomására
    madar["dy"] = madarDy #ennyi ciklusig emelkedni fog a madár
        
    

#kiszámítja két pont közötti távolságot Phitagorasz tétel alapján a koordinátákból
def tavolsag(x1, y1, x2, y2):
    tav=math.sqrt( (x2-x1)**2+(y2-y1)**2  ) # **2 jelentése a négyzeten, sqrt négyzetgyök
    return tav


def kezdes():
    global akadalySzam, akadalyok, pontszam, soronként, akadálySorTav, madar, vege
    
    vege=False
    pontszam=0
    x=ablakSzelesseg

    akadalyok=[]
    #akadályok létrehozása a látható ablakon kívűl. Ezek fognak beúszni
    for i in range(0,int(akadalySzam/soronként)):
        for j in range(0, soronként):
            akadalyok.append([x,random.randint(20, 550), random.randint(1,4)*7]) #x, y, méret
        x = x + akadálySorTav
    
    #madár alaphelyzetbe
    madar = {"x":50, "y":300, "dy":-3, "meret":10, "szin":"green"}

    jatek()


def utkozes():
    global akadalyok, madar, ablakMagassag
    
    #madar és akadály
    for akadaly in akadalyok:
        if tavolsag(madar["x"], madar["y"], akadaly[0], akadaly[1]) < madar["meret"]/2 + akadaly[2]/2 : return True

    #madar alul, vagy felül
    if madar["y"]<0 or madar["y"] > ablakMagassag : return True

    return False



def jatek():
    global pontszam, akadalyok, madar, akadályDx, vege, kezdet
    

    if kezdet:
        c.create_text(500, 120, text="Madar röptetéshez nyomj egy gombot", fill="green", font=('Helvetica 30 bold'))
        c.create_text(500, 200, text="új játékhoz ENTER", fill="yellow", font=('Helvetica 35 bold'))
        return


    if vege: return

    #Új értékek számolása
    #akadály
    for akadaly in akadalyok:
        akadaly[0] += akadályDx #akadály haladjon
        if akadaly[0]<0: #ha elérte  képernyő szélét akkor ugorjon az elejére új pozícióban és méretben
            akadaly[0]=ablakSzelesseg
            akadaly[1]=random.randint(20, 550)
            akadaly[2]=random.randint(1,4)*10
            #növelje a pontszámot
            pontszam+=1
    
    #madár - madar = {"x":50, "y":300, "dy":-3, "meret":10, "szin":"green"}
    if madar["dy"]<0:
        madar["y"]-=madarHaladas
        madar["dy"]+=1 #csökken a felrepülés ereje
    else:madar["y"]+=madarHaladas #zuhanunk


    if utkozes():
        vege=True        

    #Rajzolás új értékek szerint
    c.delete('all')
    for akadaly in akadalyok:        
        c.create_rectangle(akadaly[0]-akadaly[2]/2,
                    akadaly[1]-akadaly[2]/2,
                    akadaly[0]+akadaly[2]/2,
                    akadaly[1]+akadaly[2]/2,
                    fill="white",
                    outline="white")
    
    c.create_rectangle(madar["x"]-madar["meret"]/2,
                    madar["y"]-madar["meret"]/2,
                    madar["x"]+madar["meret"]/2,
                    madar["y"]+madar["meret"]/2,
                    fill="green",
                    outline="green")

    #Szöveg
    c.create_text(500, 50, text=str( pontszam), fill="yellow", font=('Helvetica 35 bold'))

    if vege:
        c.create_text(500, 120, text="Játék Vége - új játékhoz ENTER", fill="red", font=('Helvetica 35 bold'))
        c.create_text(500, 200, text="Madar röptetéshez nyomj egy gombot", fill="green", font=('Helvetica 30 bold'))

    sc.update() #A háttérben rajzolt tartalom megjelenítése
    sc.after(40, jatek)#jatek meghívása 40ms múlva

#Itt indul a program
if __name__ == "__main__":    
    sc = tk.Tk()# Képernyő létrehozása
    sc.title("Csapkodó Madár")#ablak címe    
    sc.geometry("1000x600")#ablak mérete
    sc.resizable(False, False)#nem lehet átméretezni
    c=tk.Canvas(sc, bg="black")#fekete rjazvászon létrehozása
    c.pack(fill="both", expand=True)#
    sc.update()#tartalom frissítése        
    sc.bind('<KeyPress>', gombLenyomas)#billentyű kezelő eljárás megadása        
    kezdes() #játék indítása
    sc.mainloop() # Minden Python Turtle programot így kell befejezni