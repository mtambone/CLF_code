#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.LTC2983 import LTC2983
from lib.LTC2983_const import *
from pyftdi.spi import SpiController

spi = SpiController()
spi.configure('ftdi://ftdi:4232h/1')
slave = spi.get_port(cs=0, freq=2E6, mode=0)

ltc = LTC2983()
adc = ltc.get_ftdi_backend(slave)

print("1. dump registers")
adc.dump_registers()

print("2. read COMMAND_STATUS register")
print(hex(adc.read_register(LTC2983.Register.COMMAND_STATUS)))

print("3. read GLOBAL_CONFIGURATION register")
print(hex(adc.read_register(LTC2983.Register.GLOBAL_CONFIGURATION)))

print("4. write 0x02 to GLOBAL_CONFIGURATION register")
adc.write_register(LTC2983.Register.GLOBAL_CONFIGURATION, 0x02)

print("5. read GLOBAL_CONFIGURATION register")
print(hex(adc.read_register(LTC2983.Register.GLOBAL_CONFIGURATION)))

print("6. read COMMAND_STATUS register")
print(hex(adc.read_register(LTC2983.Register.COMMAND_STATUS)))

print("7. read address 0x250")
print(hex(adc.read_register(0x250)))

print("8. write 0xABCDEFAF to address 0x250")
adc.write_register(0x250, 0xABCDEFAF, 4)

print("9. read address 0x250")
print(hex(adc.read_register(0x250, 4)))

adc.config_channel(2, SENSOR_TYPE__SENSE_RESISTOR |
   (10000 * 1024) << SENSE_RESISTOR_VALUE_LSB)

adc.config_channel(4, SENSOR_TYPE__THERMISTOR_CUSTOM_STEINHART_HART |
      THERMISTOR_RSENSE_CHANNEL__2 |
      THERMISTOR_DIFFERENTIAL |
      THERMISTOR_EXCITATION_MODE__SHARING_ROTATION)

print(hex(SENSOR_TYPE__THERMISTOR_CUSTOM_STEINHART_HART |
   THERMISTOR_RSENSE_CHANNEL__2 |
   THERMISTOR_DIFFERENTIAL |
   THERMISTOR_EXCITATION_MODE__SHARING_ROTATION))

from ieee754 import IEEE754
A = IEEE754(0.9059557119/1000.0, 1)
B = IEEE754(2.484884034/10000.0, 1)
D = IEEE754(2.040119886/10000000.0, 1)
adc.write_register(0x250 + 0, int(A.hex()[0], 16), 4)
adc.write_register(0x250 + 4, int(B.hex()[0], 16), 4)
adc.write_register(0x250 + 12, int(D.hex()[0], 16), 4)

#for ch in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
for ch in [6, 8, 10, 12, 14, 16, 18, 20]:
   adc.config_channel(ch, SENSOR_TYPE__THERMISTOR_44006_10K_25C |
      THERMISTOR_RSENSE_CHANNEL__2 |
      THERMISTOR_DIFFERENTIAL |
      THERMISTOR_EXCITATION_MODE__SHARING_ROTATION |
      THERMISTOR_EXCITATION_CURRENT__AUTORANGE)

print("11. read temperature from channels")
for ch in [4, 6, 8, 10, 12, 14, 16, 18, 20]:
   print(f'channel: {ch}, {round(adc.read_temperature(ch),2)} degC')

