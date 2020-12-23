#!/usr/bin/env pybricks-micropython

import struct, threading

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from devices import detectJoystick

class Robot():
    def __init__(self):
        self.motor = Motor(Port.B)
        self.ultrasonic = UltrasonicSensor(Port.S4)
        self.active = True
        self.speed = 0
        self.colors = [None, Color.GREEN, Color.YELLOW, Color.RED]

    def setSpeed(self, acc):
        if acc < 0:
            self.speed = max(-3, self.speed - 1)
        elif acc > 0:
            self.speed = min(3, self.speed + 1)
        else:
            self.speed = 0
        if self.speed != 0:
            self.motor.run(self.speed * 90)
        else:
            self.motor.stop()
        brick.light(self.colors[abs(self.speed)])

    def inactive(self):
        self.active = False
        self.setSpeed(0)
        brick.sound.beep()

def autoStopLoop(robot):
    while robot.active:
        if robot.speed > 0 and robot.ultrasonic.distance() < 200:
            robot.setSpeed(0)
        wait(100)

def joystickLoop(robot, eventFile):
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)
    with open(eventFile, 'rb') as infile:
        while True:
            event = infile.read(EVENT_SIZE)
            _, _, t, c, v = struct.unpack(FORMAT, event)
            # button A, B:
            if t == 1 and v == 1:
                if c == 305:
                    # press A:
                    robot.setSpeed(1)
                elif c == 304:
                    # press B:
                    robot.setSpeed(-1)
                elif c == 307:
                    # press X:
                    return robot.inactive()
            elif t == 3:
                if c == 1:
                    # Left stick & vertical:
                    speed = 0
                    if v < 32768:
                        # up:
                        speed = 1
                    elif v > 32768:
                        # down:
                        speed = -1
                    robot.setSpeed(speed)

def buttonLoop(robot):
    while True:
        if not any(brick.buttons()):
            wait(10)
        else:
            if Button.LEFT in brick.buttons():
                robot.setSpeed(-1)
            elif Button.RIGHT in brick.buttons():
                robot.setSpeed(1)
            elif Button.CENTER in brick.buttons():
                robot.setSpeed(0)
            elif Button.UP in brick.buttons():
                return robot.inactive()
            wait(500)

def main():
    brick.sound.beep()
    joystickEvent = detectJoystick(['Controller'])
    robot = Robot()
    t = threading.Thread(target=autoStopLoop, args=(robot,))
    t.start()
    if joystickEvent:
        joystickLoop(robot, joystickEvent)
    else:
        buttonLoop(robot)

main()
