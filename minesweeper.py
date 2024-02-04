"""
Az ismert bombakereső játék
"""
import tkinter as tk #Rajzolási eszkoz beemelése a kódba 0,0 a bal felső sarok
import random #véletlen szám generáláshoz

#LÉPÉSEK
#globális változók: pályaméret, cella méret, palya
#játékciklus
#palya feltöltése üres cellákkal
#pálya kirajzolása
#feltöltés bombákkal
#feltöltés szomszéd bombák számával
#Egérkezelés - mozgatás cella keret
#egérkezelés - kattintás jobb
#egérkezelés - kattintás bal - üres felderítés
#szamolás
#jaték vége
#ujrakezdés

#######################
## GLOBÁLIS VÁLTOZÓK ##
#######################

palyaMeret=10 #10x10 cella
bombaSzam=10
cellaMeret=60
felfedettCellak=0
maxFelfedhetoCella = palyaMeret*palyaMeret-bombaSzam
vege = False
gyozelem=False

#eger pozíció
mx=0
my=0
#palyaMeret x PalyaMeret darab cella lesz benne
palya=[]


#################################
## Saját függvények, eljárások ##
#################################

#rekurzívan felderíti a szomszédos üres cellákat
def uresFelderites(cella):
    global palya, felfedettCellak
    
    if cella["jel"]>2 or cella["bomba"]==1:
        return
    
    felfedettCellak+=1
    
    if cella["szomszed"]==0 : cella["jel"]=3
    if cella["szomszed"]!=0 : cella["jel"]=4
    
    if cella["jel"]==4:#ha vannak bomba szomszédjai, akkor vissza
        return


    fx=cella["x"]-1
    if fx<0:fx=0
    fy=cella["y"]-1
    if fy<0:fy=0

    tx=cella["x"]+2
    if tx>palyaMeret:tx=palyaMeret
    ty=cella["y"]+2
    if ty>palyaMeret:ty=palyaMeret

    for y in range(fy,ty):
        for x in range(fx,tx):
            if palya[y][x]!=cella:
                if palya[y][x]["jel"]<3 and palya[y][x]["bomba"]==0:
                    if palya[y][x]["szomszed"]>0:
                        palya[y][x]["jel"]=4
                        felfedettCellak+=1
                    else:uresFelderites(palya[y][x])
    

#Ha cellán történik, akkor felfedés
def egerKattintas1(e):
    global palya, felfedettCellak, palyaMeret, bombaSzam, vege, gyozelem

    if vege : 
        kezdes()
        return

    x=int(e.x / cellaMeret)
    y=int(e.y / cellaMeret)
    cella=palya[y][x]
    #ha még nincs felfedve
    if cella["jel"]<3:
        if cella["bomba"]==1:
            cella["jel"]=5 #bomba            
            palyaFelderites()                            
            vege = True
            gyozelem=False
    
        if cella["bomba"]==0 and cella["szomszed"]>0:
            cella["jel"]=4 #bomba szomszed
            felfedettCellak+=1    
        
        if cella["bomba"]==0 and cella["szomszed"]==0:
            #cella["jel"]=3 #ures
            uresFelderites(cella)
        
        if palyaMeret*palyaMeret-felfedettCellak == bombaSzam:
            palyaFelderites()
            vege = True
            gyozelem = True



#Információs kattintás
def egerKattintas3(e):

    if vege : return

    x=int(e.x / cellaMeret)
    y=int(e.y / cellaMeret)
    #print("x:",x,"y:",y)
    cella=palya[y][x]
    if cella["jel"]<3:
        cella["jel"]=cella["jel"]+1
        if cella["jel"]>2:cella["jel"]=0



def egerMozgas(e):
    global mx, my

    if vege : return

    mx=e.x
    my=e.y


#Felfed mindent
def palyaFelderites():
    for y in range(palyaMeret):            
        for x in range(palyaMeret):
            if palya[y][x]["jel"]<3:                        
                if palya[y][x]["szomszed"]==0:
                    palya[y][x]["jel"]=3
                else : palya[y][x]["jel"]=4

                if palya[y][x]["bomba"]==1:
                    palya[y][x]["jel"]=5

def jatek():
    global c, felfedettCellak, palyaMeret, bombaSzam, cellaMeret, mx, my, palya

    #[kirajzolás]
    c.delete('all') #korábbi tartalom törlése, új képkocka rajzolás megkezdéséhez

    for y in range(palyaMeret):
        for x in range(palyaMeret):            
            cella=palya[y][x]
            #cella keretének megrajzolása
            szin="grey" #felfedetlen
            txtSzin="blue"  
            outlineSzin="blue"          
            #txt=str(s)
            txt=""

            #felfedett
            if cella["jel"]==3:
                szin="white"
                txt=""

            if cella["jel"]==4:
                txt=str(cella["szomszed"])
                szin="lightGreen"

            if cella["jel"]==5:
                txt="*"
                txtSzin="red"

            #felfedettlen
            if cella["jel"]==1:
                txt="!"
            if cella["jel"]==2:
                txt="?"

            #teszteléshez könnyítés - jelzi a bombát
            #if cella["bomba"]==1 : txtSzin="red"

            c.create_rectangle(cella["x"]*cellaMeret,
                               cella["y"]*cellaMeret,
                               cella["x"]*cellaMeret+cellaMeret,
                               cella["y"]*cellaMeret+cellaMeret,
                               fill=szin,
                               outline=outlineSzin
                               )
            #cella szöveg kiírása
            if txt!="":
                c.create_text(cella["x"]*cellaMeret+cellaMeret/2,
                          cella["y"]*cellaMeret+cellaMeret/2, 
                          text=txt, 
                          fill=txtSzin, 
                          font=('Helvetica 18 bold'))           
    
    #cella aktiválás eger kurzor alatt
    if mx<palyaMeret*cellaMeret and my<palyaMeret*cellaMeret :
        c.create_rectangle(int(mx / cellaMeret) * cellaMeret,
                               int(my / cellaMeret) * cellaMeret,
                               int(mx / cellaMeret) * cellaMeret + cellaMeret,
                               int(my / cellaMeret) * cellaMeret + cellaMeret,                               
                               outline="red",
                               width=3
                               )

    c.create_text(palyaMeret*cellaMeret/2, palyaMeret*cellaMeret+cellaMeret/2,
                          text="Felderitetlen cellák: "+str(palyaMeret*palyaMeret-felfedettCellak-bombaSzam), 
                          fill="yellow", 
                          font=('Helvetica 18 bold'))
    
    #Vége
    if vege:
        if gyozelem : text = "Nyertél!"
        else : text = "Vesztettél!"
        c.create_text(palyaMeret*cellaMeret/2, palyaMeret*cellaMeret+cellaMeret*1.5,
                          text=text, 
                          fill="white", 
                          font=('Helvetica 20 bold'))


    #A háttérben rajzolt tartalom megjelenítése
    sc.update() 
    
    sc.after(100, jatek)#jatek eljárás újbóli meghívása 30ms múlva


def szomszedBomba(cella):
    global palya
    
    fx=cella["x"]-1
    if fx<0:fx=0
    fy=cella["y"]-1
    if fy<0:fy=0

    tx=cella["x"]+2
    if tx>palyaMeret:tx=palyaMeret
    ty=cella["y"]+2
    if ty>palyaMeret:ty=palyaMeret
    szomszed=0

    for y in range(fy,ty):
        for x in range(fx,tx):
            if palya[y][x]["bomba"]==1:szomszed=szomszed+1

    #ki kell vonni magamat ha én bomba vagyok
    if szomszed>0 and cella["bomba"]==1:szomszed=szomszed-1

    return szomszed



def kezdes():
    global palya, palyaMeret, cellaMeret, felfedettCellak, vege, gyozelem
    vege=False
    gyozelem=False
    felfedettCellak=0
    palya=[]
    sor = []
    #pálya mátrix feltöltése cellákkal
    for y in range(palyaMeret):
        sor = []
        for x in range(palyaMeret):
            ##cella={"x":1, "y":1, "size":30, "bomba":1, "szomszed":0, "jel":0}
            cella={"x":x, "y":y, "size":cellaMeret, "bomba":0, "szomszed":0, "jel":0}
            sor.append(cella)
        palya.append(sor)

    #bombák elhelyezése
    for i in range(bombaSzam):
        tovabb=True
        while tovabb:
            bx=random.randint(0,9)
            by=random.randint(0,9)
            cella=palya[by][bx]
            if cella["bomba"]==0:
                cella["bomba"]=1
                tovabb=False
            
    #szomszédos bombák kiszámolása
    for y in range(palyaMeret):
        for x in range(palyaMeret):
            cella=palya[y][x]
            cella["szomszed"]=szomszedBomba(cella)
    #játékciklus indítása
    jatek()


#############################
## PROGRAM BELÉPÉSI PONTJA ##
#############################
#Itt indul a program
if __name__ == "__main__":    
    sc = tk.Tk()# Grafikus ablak létrehozása
    sc.title("Aknakereső")#ablak címe    
    sc.geometry("1000x600")#ablak mérete
    sc.geometry(str(palyaMeret*cellaMeret)+"x"+str(palyaMeret*cellaMeret+2*cellaMeret))#ablak mérete
    sc.config(cursor="plus") #célkereszt legyen a kurzor cross
    sc.resizable(False, False)#nem lehet átméretezni

    #fekete rajzvászon létrehozása
    c=tk.Canvas(sc, bg="black")
    c.pack(fill="both", expand=True)#

    sc.bind('<ButtonPress-1>', egerKattintas1) #Egér kattintást kezelő regisztrálása
    sc.bind('<ButtonPress-3>', egerKattintas3) #Egér kattintást kezelő regisztrálása
    sc.bind('<Motion>', egerMozgas) #Egérmozgást kezelő regisztrálása

    sc.update()#tartalom frissítése        

    #játék indítása
    kezdes()
    

    sc.mainloop() # Minden Python Tk programot így kell befejezni
