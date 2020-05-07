#!/usr/bin/env pybricks-micropython

import struct, threading

from pybricks import ev3brick as brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color, SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase

from devices import detectJoystick
from joystick import JoyStick, BUTTON_A, BUTTON_X

SPEED = 100
STEERING = 90

STATUS_STOPPED = 0
STATUS_FORWARD = 1
STATUS_BACKWARD = 2
STATUS_STEERING = 3

COLORS = (None, Color.GREEN, Color.RED, Color.YELLOW)

class Driver():
    def __init__(self, leftMotor, rightMotor, diameter, axle):
        self.driver = DriveBase(leftMotor, rightMotor, diameter, axle)
        self.x = 0
        self.y = 0
        self.speed = 0
        self.steering = 0

    def drive(self, speed, steering):
        self.speed = speed
        self.steering = steering
        if self.speed == 0:
            self.driver.stop()
        else:
            self.driver.drive(self.speed, self.steering)

class Robot():
    def __init__(self, leftMotor, rightMotor, topMotor, diameter, axle, maxSpeed=300, maxSteering=180, port=Port.S4):
        self.driver = Driver(leftMotor, rightMotor, diameter, axle)
        self.cannon = topMotor
        self.ultrasonic = UltrasonicSensor(port)
        self.speedStep = 32767 // maxSpeed
        self.steeringStep = 32767 // maxSteering
        self.active = True

    def drive(self, x, y):
        # map y (-32768 ~ +32767) to speed (+maxSpeed ~ -maxSpeed):
        speed = -y // self.speedStep
        # map x (-32768 ~ +32767) to steering (-maxSteering ~ +maxSteering):
        steering = x // self.steeringStep
        self.driver.drive(speed, steering)

    def target(self, x):
        self.cannon.run(-x // 327)

    def fire(self):
        brick.sound.file('cannon.wav')

    def inactive(self):
        self.active = False
        self.drive(0, 0)
        brick.sound.beep()

def autoStopLoop(robot):
    while robot.active:
        if robot.ultrasonic.distance() < 200:
            robot.drive(0, 0)
        wait(100)

def main():
    brick.sound.beep()
    joystickEvent = detectJoystick(['Controller'])
    if joystickEvent:
        robot = Robot(Motor(Port.D), Motor(Port.A), Motor(Port.B), 55, 200)
        t = threading.Thread(target=autoStopLoop, args=(robot,))
        t.start()

        def onButtonPressed(code):
            if code == BUTTON_X:
                robot.inactive()
                return False
            if code == BUTTON_A:
                robot.fire()
            return True

        def onLeftJoyChanged(x, y):
            robot.drive(x, y)

        def onRightJoyChanged(x, y):
            robot.target(x)

        joystick = JoyStick(joystickEvent)
        joystick.setButtonHandler(onButtonPressed)
        joystick.setJoyLeftHandler(onLeftJoyChanged)
        joystick.setJoyRightHandler(onRightJoyChanged)
        joystick.startLoop()
    else:
        brick.sound.beep()

main()
