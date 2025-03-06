#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.FPGARunControl import FPGARunControl

rc = FPGARunControl("/dev/runcontrol")
rc.connect()

print("1. dump FPGA registers (0-16)")
for reg in range(0,16):
   print(hex(rc.read_register(reg)))

print("2. write 0xABCD in register 13")
rc.write_register(13, 0xABCD)

print("3. read register 13")
print(hex(rc.read_register(13)))

rc.close()
