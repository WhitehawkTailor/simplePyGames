"""
H-Tree Fractal using recursion and Turtle Graphics.
Robin Andrews - https://compucademy.net/
"""
import tkinter as tk


#Globális változok
#Ablak létrehozása
win = tk.Tk() 
#Ablak címe
win.title("Háromszög Fraktál")
#ablak ikon
#win.iconbitmap("ikon.ico")
#ablak méretezése
win.geometry("800x800")
#vászon canvas - Az ablak rajzolható területe
c = tk.Canvas(win, bg="black") #bal felső sarok a 0,0
c.pack(fill="both", expand=True)#both: töltse ki a vászon az ablakot és átméretezéskor is mindíg tölse ki
win.update()
color='red'


def draw_line(pos1, pos2):
    global color
    c.create_line(pos1[0], pos1[1],pos2[0], pos2[1],fill=color)
    

def recursive_draw(x, y, size, count):
    #Ne legyen 5-nél több rekurziós mélység
    if count>10:count=10
    
    #segédváltozó a háromszög magassága
    distance = round(size*1,73205080757//2) #négyzetgyök 3=1,73...

    #rajzolás    
    draw_line([x, y],[x+size, y])#alap vonal
    draw_line([x, y],[x+size//2, y-distance] )#/ bal szára
    draw_line([x+size//2, y-distance],[x+size, y] )#\ jobb szára
    
    win.update()
    
    if count <= 0:  # Rekurziós mélység kezelése, ha elérte a legmélyebb pontot, akkor kiugruk
        return
    else:  # egyébként valósítsa meg a rekurziós hívásokat
        count -= 1 #rekurzió mélység közelítése a határhoz
        #segéd változók kiszámítása
        ujmeret = size//2
        recursive_draw(x, y, ujmeret, count)
        recursive_draw(x+ujmeret, y, ujmeret, count)
        recursive_draw(x+size//4, y-distance//2, ujmeret, count)
        

def start():
    global color
    color='red'    
    recursive_draw(10, 790, 780, 8)
    color='white'
    recursive_draw(10, 790, 780, 6)
    color='green'
    recursive_draw(10, 790, 780, 4)
    win.update()


if __name__ == "__main__":
    # Rekurzió első hívása
    win.after(500,start())
    win.mainloop()
    