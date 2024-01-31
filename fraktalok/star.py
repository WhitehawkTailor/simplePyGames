
# import turtle 
import turtle 
  
# initialise turtle instance 
stars = turtle.Turtle() 
  
# increases the speed of turtle 
stars.speed(0) 
  
# to change the background color 
stars.getscreen().bgcolor("black") 
stars.color("red") 
  
# stop drawing 
stars.penup() 
stars.hideturtle()

# move the turtle 
stars.goto((-200, 50)) 
  
# start drawing 
stars.pendown() 
  
# function to draw stars 
def star(turtle, size): 
    if size <= 10: 
        return
    else: 
        for i in range(5): 
            
            # moving turtle forward 
            turtle.forward(size) 
            star(turtle, size/3) 
  
            # moving turtle left             
            turtle.left(216) #fordulj 216 fokot
  
  
# calling the star function 
#star(stars, 360) 
star(stars, 360) 
turtle.done() 
