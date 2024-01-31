"""
H-Tree Fractal using recursion and Turtle Graphics.
Robin Andrews - https://compucademy.net/
"""
import turtle



def draw_line(pen, pos1, pos2):
    # print("Drawing from", pos1, "to", pos2)  # Uncomment for tracing the algorithm.
    pen.penup()
    pen.goto(pos1[0], pos1[1])
    pen.pendown()
    pen.goto(pos2[0], pos2[1])

def recursive_draw(pen, x, y, size, count):
    #Ne legyen 5-nél több rekurziós mélység
    if count>5:count=5
    
    #segédváltozó a háromszög magassága
    distance = round(size*1,73205080757//2) #négyzetgyök 3=1,73...

    #rajzolás    
    draw_line(pen,[x, y],[x+size, y])#alap vonal
    draw_line(pen,[x, y],[x+size//2, y+distance] )#/ bal szára
    draw_line(pen,[x+size//2, y+distance],[x+size, y] )#\ jobb szára
    
    if count <= 0:  # Rekurziós mélység kezelése, ha elérte a legmélyebb pontot, akkor kiugruk
        return
    else:  # egyébként valósítsa meg a rekurziós hívásokat
        count -= 1 #rekurzió mélység közelítése a határhoz
        #segéd változók kiszámítása
        ujmeret = size//2
        recursive_draw(pen, x, y, ujmeret, count)
        recursive_draw(pen, x+ujmeret, y, ujmeret, count)
        recursive_draw(pen, x+size//4, y+distance//2, ujmeret, count)
        


if __name__ == "__main__":
    # képernyő beállítások
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.title("Háromszög fraktál")
    screen.bgcolor("black")

    # Turtle rajzoló (pen, toll) beállítása
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.pensize(2)    
    pen.speed(0)
    pen.color("red") #toll színének beállítása

    # Rekurzió első hívása
    recursive_draw(pen, -390, -390, 780, 5)
    # Minden Python program, ami használja a Turtle-t ezzel kell, hogy kilépjen
    turtle.done()