# joystick control:

import struct

# define button code:

BUTTON_A = 305
BUTTON_B = 304
BUTTON_X = 307
BUTTON_Y = 306
BUTTON_PLUS = 313
BUTTON_MINUS = 312
BUTTON_START = 317
BUTTON_HOME = 316 

class JoyStick():
    def __init__(self, eventFile):
        self.eventFile = eventFile
        self.buttonHandler = None
        self.joyLeftHandler = None
        self.joyRightHandler = None

    def setButtonHandler(self, buttonHandler):
        self.buttonHandler = buttonHandler

    def setJoyLeftHandler(self, joyLeftHandler):
        self.joyLeftHandler = joyLeftHandler

    def setJoyRightHandler(self, joyRightHandler):
        self.joyRightHandler = joyRightHandler

    def startLoop(self):
        FORMAT = 'llHHI'
        EVENT_SIZE = struct.calcsize(FORMAT)
        with open(self.eventFile, 'rb') as infile:
            lx, ly, rx, ry = 0, 0, 0, 0
            while True:
                event = infile.read(EVENT_SIZE)
                _, _, t, c, v = struct.unpack(FORMAT, event)
                if t == 1 and v == 1:
                    # button pressed:
                    if self.buttonHandler:
                        if not self.buttonHandler(c):
                            return
                if t == 3:
                    if c == 0 and self.joyLeftHandler:
                        # left stick & horizontal:
                        lx = v - 32768
                        self.joyLeftHandler(lx, ly)
                    elif c == 1 and self.joyLeftHandler:
                        # left stick & vertical:
                        ly = v - 32768
                        self.joyLeftHandler(lx, ly)
                    elif c == 3 and self.joyRightHandler:
                        # right stick & horizontal:
                        rx = v - 32768
                        self.joyRightHandler(rx, ry)
                    elif c == 4 and self.joyRightHandler:
                        # right stick & vertical:
                        ry = v - 32768
                        self.joyRightHandler(rx, ry)
