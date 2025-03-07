import os
import sys
import serial
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.RPC import RPCDevice
from lib.VXM import VXM

class DeviceCollection:
    def __init__(self):
        self.serials = {}
        self.outlets = {}
        self.motors = {}

    def add_outlet(self, id, name, port, speed=115200, bytesize=8, parity='N', stopbits=1, timeout=1):
        if(self.serials.get(port, None) == None):
            s = serial.Serial(
                    port=port, 
                    baudrate=speed, 
                    bytesize=bytesize, 
                    parity=parity,
                    stopbits = stopbits,
                    timeout = timeout)
            self.serials[port] = RPCDevice(s)

        rpc = self.serials[port]
        self.outlets[name] = rpc.add_outlet(id, name)

    def get_outlet(self, name):
        return self.outlets[name]

    def add_motor(self, id, name, port, speed=115200, bytesize=8, parity='N', stopbits=1, timeout=1):
        if(self.serials.get(port, None) == None):
            s = serial.Serial(
                    port=port, 
                    baudrate=speed, 
                    bytesize=bytesize, 
                    parity=parity,
                    stopbits = stopbits,
                    timeout = timeout)
            self.serials[port] = VXM(s)

        vxm = self.serials[port]
        self.motors[name] = vxm.add_motor(id, name)

    def get_motor(self, name):
        return self.motors[name]


    def __repr__(self):
        return f'{self.outlets}'

if __name__ == "__main__":
    dc = DeviceCollection()

    dc.add_outlet(0, "PC", "/dev/ttyUSB0")
    dc.add_outlet(1, "RAMAN1", "/dev/ttyUSB0")
    print(dc)

    dc.get_outlet("PC").on()
    dc.get_outlet("RAMAN1").on()

