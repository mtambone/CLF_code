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


def test_centurion():
    c = Centurion("/dev/ttyr00", )
    time.sleep(1)
    c.read_bytes()
    print("CENT_TEST:TEST COMPLETE SUCCESSFULLY")


def test_RPC():
    rpc= RPCDevice('COM6')

    out1 = rpc.add_outlet(0, "RAMAN")
    #out1.on()
    out1.status()
    #out1.off()
    print("RPC_TEST:TEST COMPLETE SUCCESSFULLY")

def test_VXM():
    vxm = VXM("/dev/ttyr00")
    vxm.move_ABS0(1)
    vxm.move_Neg0(1)
    vxm.move_Pos0(1)
    vxm.move_ABS0(1)
    print("VXM_TEST:TEST COMPLETE SUCCESSFULLY")

def test_radiometer():
    radio = Rad_Monitor_3700('COM6')
    radio.rad_info()
    radio.rad_set()
    #radio.check_parameter()


if __name__ == "__main__":
    test_radiometer()
    
