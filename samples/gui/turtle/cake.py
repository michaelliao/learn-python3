# creating a cake of pink color


# importing turtle module
import turtle

# creating turtle object
tut = turtle.Turtle()
# initialize turtle window
new = turtle.getscreen()
# setting gackground color
new.bgcolor("lightblue")
# setting position of turtle to middle of window
tut.home()
# start drawing
tut.pendown()
# changing color
tut.color("hotpink")
# setting width of width of stroked
tut.width(3)
# setting speed of turtle
tut.speed(0)


def squre(length, angle):
    # Drawing 4 sides of a square
    tut.forward(length)
    tut.right(angle)
    tut.forward(length)
    tut.right(angle)
    tut.forward(length)
    tut.right(angle)
    tut.forward(length)
    tut.right(angle)


squre(80, 90)

# 36 * 10  = 360 for a complete circle tracing
for i in range(36):
    tut.right(10)
    squre(80, 90)
