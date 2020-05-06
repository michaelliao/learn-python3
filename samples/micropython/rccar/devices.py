# list input devices

class InputDevice():
    def __init__(self):
        self.name = ''
        self.handler = ''

    def __str__(self):
        return '<Input Device: name=%s, handler=%s>' % (self.name, self.handler)

    def setName(self, name):
        if len(name) >= 2 and name.startswith('"') and name.endswith('"'):
            name = name[1:len(name)-1]
        self.name = name

    def setHandler(self, handlers):
        for handler in handlers.split(' '):
            if handler.startswith('event'):
                self.handler = handler

def listDevices():
    devices = []
    with open('/proc/bus/input/devices', 'r') as f:
        device = None
        while True:
            s = f.readline()
            if s == '':
                break
            s = s.strip()
            if s == '':
                devices.append(device)
                device = None
            else:
                if device is None:
                    device = InputDevice()
                if s.startswith('N: Name='):
                    device.setName(s[8:])
                elif s.startswith('H: Handlers='):
                    device.setHandler(s[12:])
    return devices

def detectJoystick(joystickNames):
    for device in listDevices():
        for joystickName in joystickNames:
            if joystickName in device.name:
                return '/dev/input/%s' % device.handler
    return None
