import sys
import os
import time

lib_path = os.path.abspath('C:/Users/130847/Desktop/Auger/CLF_code/lib')

# Append it to sys.path
sys.path.append(lib_path)

from Centurion import Centurion
from VXM import VXM
from Radiometer import Rad_Monitor_3700, Rad_Ophir
from RPC import RPCDevice 

def main(self):

    cent = Centurion("/dev/ttyr00", )
    rpc= RPCDevice('COM6')
    vxm = VXM("/dev/ttyr00")
    radio = Rad_Monitor_3700('COM6')

    out_raman = rpc.add(0, "RAMAN")
    out_radio = rpc.add(1, "RADM")
    out_lsr = rpc.add(2, "LASER")

    out_raman.on()
    out_raman.status()
    out_radio.on()
    out_radio.status()
    out_lsr.on()
    out_lsr.status()

    radio = Rad_Monitor_3700('COM6')
    radio.rad_info()
    radio.rad_set()

    cent.check_temps()
    cent.warmup()
    cent.fire()

if __name__ == "__main__":
    main()

