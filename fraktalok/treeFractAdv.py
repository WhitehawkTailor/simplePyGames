"""
Fa fraktál kirajzoló program
Minden ág végére rakjon 3 új rövidebb ágat különböző irányokban

Turtle rajzoló eszköz használat
#https://docs.python.org/3/library/turtle.html
"""

#Rajzolási eszkoz beemelése a kódba
import tkinter as tk
import math


#Globális változok
#Ablak létrehozása
win = tk.Tk() 
#Ablak címe
win.title("Háromszög Fraktál")
#ablak ikon
#win.iconbitmap("ikon.ico")
#ablak méretezése
win.geometry("1000x800")
#vászon canvas - Az ablak rajzolható területe
c = tk.Canvas(win, bg="black") #bal felső sarok a 0,0
c.pack(fill="both", expand=True)#both: töltse ki a vászon az ablakot és átméretezéskor is mindíg tölse ki
win.update()
posX=500
posY=800
angle=90


#Saját szín skála
#szinek = ["black","gray", "darkgreen", "green", "cyan", "white"]
szinek = ["white","yellow", "cyan", "green", "darkgreen","gray", "darkgrey"]


def drawLine(x, y, direction, size, color):
    global posX, posY
    #vonal vége koordináták kiszámolása
    posX=x+size*math.sin(direction*math.pi/180)
    posY=y+size*math.cos(direction*math.pi/180)
    c.create_line(x, y, posX, posY, fill=color)
    win.update()



#Rekurzív rajzoló eljárás
#Azért rekurzív, mert önmagát meghívja
#A kialakuló ábra attól függ, hogy az önhívások milyen számban és milyen paraméter változással történnek meg.
#
#A rutin kirajzol egy egyenest és az egyenes végéből indulva meghívja saját magát többször.
#Ahány hivást kezdeményez, annyi elágazás lesz egy ág végén
#Az elágazások hossza a megkapott hossz osztásával történik, ezért minden rekurzív hívási mályságben egyre rövidebbek az ágak
#Az ágak szögei pedig hivási vonalanként összeadódnak, ezért ágaznak el egymástól az ágak egyre jobban
#recursive_draw(pen, 0, 400, 300, 90, 5)
def recursive_draw(x, y, size, direction, count):
    global posX, posY
    #rekurzió mélység maximalizálása
    if count>6: count=6

    #rajzolja meg a vonalat    
    drawLine(x, y, direction, size, szinek[count] )

    if count <= 0:  #Rekurzió mélység
        return
    else:  # A rekúrzív hívások
        count -= 1 #csökkentse a rekúrzív mélységet
        #Hívja meg az új rajzolásokat - hány új ága van egy ágnak és milyen paraméterekkel
#       V1
#        recursive_draw(pen, nx, ny, size*0.65, direction+45, count)
#        recursive_draw(pen, nx, ny, size*0.65, direction, count)
#        recursive_draw(pen, nx, ny, size*0.65, direction-45, count)
        nx=posX
        ny=posY
        recursive_draw(nx, ny, size*0.65, direction+90, count)
        recursive_draw(nx, ny, size*0.65, direction, count)
        recursive_draw(nx, ny, size*0.65, direction-90, count)


def start():    
    global posX, posY, szinek
    #recursive_draw( posX, posY-50, 300, 180, 1)  #V0
    #recursive_draw(posX, posY, -400, 250, 90, 6)  #V1
    recursive_draw( posX, posY-50, 250, 180, 6)  #V2


#Itt indul a program
if __name__ == "__main__":
    # Rekurzió első hívása
    win.after(500,start())
    win.mainloop()
    