#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.TLA2518 import TLA2518
from pyftdi.spi import SpiController

spi = SpiController()
spi.configure('ftdi://ftdi:4232h/2')
slave = spi.get_port(cs=0, freq=30E6, mode=0)

tla = TLA2518()
adc = tla.get_ftdi_backend(slave)


for ch in range(0, 8):
    print(f'AIN{ch}: {adc.read_channel(ch)*12}')
