
from time import sleep
from enum import Enum
from functools import reduce
from pyftdi.spi import SpiController
from lib.LTC2983_const import *

class LTC2983_Base:

   class Register:
      COMMAND_STATUS = 0x0000
      GLOBAL_CONFIGURATION = 0x00F0
      MUX_DELAY = 0x00FF

   def __init__(self):
      # temperature in Celsius, rejection 50Hz/60Hz
      self.write_register(self.Register.GLOBAL_CONFIGURATION, 
         REJECTION__50_60_HZ | TEMP_UNIT__C)
      # set mux delay to 0
      self.write_register(self.Register.MUX_DELAY, 0x00)

   def config_channel(self, ch, data):
      addr = 0x200 + (4 * (ch - 1))
      self.write_register(addr, data, 4)

   def read_channel(self, ch):
      self.write_register(self.Register.COMMAND_STATUS, (0x80 | ch))
      while True:
         if self.read_register(self.Register.COMMAND_STATUS) & 0x40:
            break
         sleep(0.05)
      value = self.read_register(READ_CH_BASE + (4 * (ch - 1)), 4)
     
      return value

   def read_temperature(self, ch):
      return self.signed_to_temperature(self.raw_to_signed(self.read_channel(ch)))

   def raw_to_signed(self, value):
      x = 0
      sign = False
      # convert a 24-bit two's complement number into a 32-bit two's complement number
      x = value & 0x00FFFFFF
      if value & 0x00800000:
         x = x | 0xFF000000

      return x

   def signed_to_temperature(self, value):
      return value / 1024.0

   def dump_registers(self):
      print(f'COMMAND_STATUS addr: 0x0000, value: {hex(self.read_register(self.Register.COMMAND_STATUS))}')
      print(f'GLOBAL_CONFIGURATION addr: 0x0000, value: {hex(self.read_register(self.Register.GLOBAL_CONFIGURATION))}')
      print(f'MUX_DELAY addr: 0x0000, value: {hex(self.read_register(self.Register.MUX_DELAY))}')
   
class LTC2983_FTDI(LTC2983_Base):

   def __init__(self, slave):
      self.spi = slave
      super().__init__()

   def read_register(self, addr, nbytes=1):
      l = list(self.spi.exchange([RD_REG, ((addr & 0xFF00) >> 8), (addr & 0xFF)], nbytes))
      return reduce(lambda x, y: x * 0x100 + y, l)

   def write_register(self, addr, value, nbytes=1):
      l = [WR_REG, ((addr & 0xFF00) >> 8), (addr & 0xFF)]
      l.extend(value.to_bytes(nbytes))
      self.spi.write(l)

class LTC2983(LTC2983_Base):

   def __init__(self):
      None

   def get_ftdi_backend(self, slave):
      return LTC2983_FTDI(slave) 
