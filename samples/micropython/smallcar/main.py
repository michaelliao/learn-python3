#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

# Write your program here

motor = Motor(Port.B)
ultrasonic = UltrasonicSensor(Port.S4)

brick.sound.beep()
brick.light(None)

speed = 0
colors = [None, Color.GREEN, Color.YELLOW, Color.RED]

def setSpeed(acc):
    global speed
    if acc < 0:
        speed = max(0, speed - 1)
    elif acc > 0:
        speed = min(3, speed + 1)
    else:
        speed = 0
    if speed > 0:
        motor.run(speed * 90)
    else:
        motor.stop()
    brick.light(colors[speed])

while True:
    if not any(brick.buttons()):
        wait(10)
    else:
        if Button.LEFT in brick.buttons():
            setSpeed(-1)
        elif Button.RIGHT in brick.buttons():
            setSpeed(1)
        elif Button.CENTER in brick.buttons():
            setSpeed(0)
        elif Button.UP in brick.buttons():
            setSpeed(0)
            break
        wait(500)
    if ultrasonic.distance() < 200:
        setSpeed(0)

brick.sound.beep()
