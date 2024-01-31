"""
Fa fraktál kirajzoló program
Minden ág végére rakjon 3 új rövidebb ágat különböző irányokban

Turtle rajzoló eszköz használat
#https://docs.python.org/3/library/turtle.html
"""

#Rajzolási eszkoz beemelése a kódba
import turtle


#Saját szín skála
#szinek = ["black","gray", "darkgreen", "green", "cyan", "white"]
szinek = ["white","yellow", "cyan", "green", "darkgreen","gray", "darkgrey"]

#Rekurzív rajzoló eljárás
#Azért rekurzív, mert önmagát meghívja
#A kialakuló ábra attól függ, hogy az önhívások milyen számban és milyen paraméter változással történnek meg.
#
#A rutin kirajzol egy egyenest és az egyenes végéből indulva meghívja saját magát többször.
#Ahány hivást kezdeményez, annyi elágazás lesz egy ág végén
#Az elágazások hossza a megkapott hossz osztásával történik, ezért minden rekurzív hívási mályságben egyre rövidebbek az ágak
#Az ágak szögei pedig hivási vonalanként összeadódnak, ezért ágaznak el egymástól az ágak egyre jobban
#recursive_draw(pen, 0, 400, 300, 90, 5)
def recursive_draw(pen, x, y, size, direction, count):
    #rekurzió mélység maximalizálása
    if count>6: count=6

    #rajzolja meg a vonalat    
    pen.penup()#emelje fel a tollat
    pen.goto(x, y)#vigye az új pozícióba
    pen.setheading(direction)#állítsa be az új irányt
    pen.color(szinek[count]) #vonal szín beállítása saját színskála alapján
    #pen.color("green") #vonal szín beállítása
    pen.pendown()#tegye le a tollat
    pen.forward(size)#nemjen előre

    #új pozíció megjegyzése
    nx=round(pen.xcor())#kérje el az új hely X koordinátáját
    ny=round(pen.ycor())#kérje el az új hely X koordinátáját
    
    if count <= 0:  #Rekurzió mélység
        return
    else:  # A rekúrzív hívások
        count -= 1 #csökkentse a rekúrzív mélységet
        #Hívja meg az új rajzolásokat - hány új ága van egy ágnak és milyen paraméterekkel
#       V1
#        recursive_draw(pen, nx, ny, size*0.65, direction+45, count)
#        recursive_draw(pen, nx, ny, size*0.65, direction, count)
#        recursive_draw(pen, nx, ny, size*0.65, direction-45, count)
        recursive_draw(pen, nx, ny, size*0.65, direction+90, count)
        recursive_draw(pen, nx, ny, size*0.65, direction, count)
        recursive_draw(pen, nx, ny, size*0.65, direction-90, count)


#Itt indul a program
if __name__ == "__main__":
    # Képernyő beállítás
    screen = turtle.Screen()# képernyő változó elkérése
    screen.setup(1000, 800) # ablak méret beállítása
    screen.title("Fa fraktál") #ablak címének beállítása
    screen.bgcolor("black") #fekete alap szín beállítása

    # A rajzolási paraméterek megadása. Turtle toll (pen) beállítása
    pen = turtle.Turtle() # a rajzolo változó elkérése. A 0,0 pont a képernyő közepe
    pen.hideturtle() #Fej kirajzolás letiltása
    pen.pensize(1) #vonal vastagság beállítása       
    pen.speed(0) #rajzolás gyorsasága - 0 a leggyorsabb

    # A rekúrzív rajzolás első hívása
    #          pen, x,   y,  mérete, iránya, rekurzió mélysége
    
    #recursive_draw(pen, 0, -400, 250, 90, 6)  #V1
    recursive_draw(pen, 0, -400, 300, 90, 5)  #V2

    # Minden Python Turtle programot így kell befejezni
    turtle.done()