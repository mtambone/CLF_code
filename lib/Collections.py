import serial

class MotorCollection:
    def __init__(self):
        self.motors = {}
        self.serials = {}

    def add(self, id, name, port, speed=115200, bytesize=8, parity='N', stopbits=1, timeout=1):
        # create here serial object and track for same port usage
        # from different channels
        if(self.serials.get(port, None) == None):
            self.serials[port] = serial.Serial(
                    port=port, 
                    baudrate=speed, 
                    bytesize=bytesize, 
                    parity=parity,
                    stopbits = stopbits,
                    timeout = timeout)
        self.motors[name] = Motor(self.serials[port], id, name)

    def get(self, attr):
        return self.motors[attr]

    def __repr__(self):
        return f'{self.motors}'

class Motor:
    def __init__(self, port, id, name):
        self.ser = port
        self.id = id
        self.name = name

    def move(self, pos):
        print(f"moving motor {self.name} with id {self.id} to {pos}")

    def __repr__(self):
        return f'({self.id}, {self.name}, {self.ser})'


if __name__ == "__main__":
    mc = MotorCollection()

    mc.add(0, "NorthSud", "/dev/ttyUSB0")
    mc.add(1, "EastWest", "/dev/ttyUSB0")
    print(mc)

    mc.get("NorthSud").move(10)
    mc.get("EastWest").move(20)

