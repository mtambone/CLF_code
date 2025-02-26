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

print("1. dump TLA2518 registers")
adc.dump_registers()

print("2. set manual mode and read channels")
adc.set_mode(TLA2518.Mode.MANUAL)
adc.dump_channels()

print("3. set on-the-fly mode and read channels")
adc.set_mode(TLA2518.Mode.ON_THE_FLY)
adc.dump_channels()

print("4. set low sampling frequency and read channels")
adc.set_high_sampling_freq(TLA2518.LowSamplingFreq.N0P16_KSPS)
adc.dump_channels()
