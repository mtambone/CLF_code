
from enum import Enum
from pyftdi.spi import SpiController

# op codes
RD_REG = 0x10
WR_REG = 0x08
SET_BIT = 0x18
CLR_BIT = 0x20

class TLA2518_Base:

   class Register(Enum):
      SYSTEM_STATUS = 0x00
      GENERAL_CFG = 0x01
      DATA_CFG = 0x02
      OSR_CFG = 0x3
      OPMODE_CFG = 0x4
      PIN_CFG = 0x5
      GPIO_CFG = 0x7
      GPO_DRIVE_CFG = 0x9
      GPO_VALUE = 0xB
      GPI_VALUE = 0xD
      SEQUENCE_CFG = 0x10
      CHANNEL_SEL = 0x11
      AUTO_SEQ_CH_SEL = 0x12

   class Mode(Enum):
      MANUAL = 0x00
      AUTO_SEQUENCE = 0x01
      ON_THE_FLY = 0x02

   class HighSamplingFreq(Enum):
      N1000_KSPS = 0x0
      N666P7_KSPS = 0x1
      N500_KSPS = 0x2
      N333P3_KSPS = 0x3
      N250_KSPS = 0x4
      N166P7_KSPS = 0x5
      N125_KSPS = 0x6
      N83_KSPS = 0x7
      N62P5_KSPS = 0x8
      N41P7_KSPS = 0x9
      N31P3_KSPS = 0xA
      N20P8_KSPS = 0xB
      N15P6_KSPS = 0xC
      N10P4_KSPS = 0xD
      N7P8_KSPS = 0xE
      N5P2_KSPS = 0xF
      
   class LowSamplingFreq(Enum):
      N31P25_KSPS = 0x0
      N20P83_KSPS = 0x1
      N15P63_KSPS = 0x2
      N10P42_KSPS = 0x3
      N7P81_KSPS = 0x4
      N5P21_KSPS = 0x5
      N3P91_KSPS = 0x6
      N2P60_KSPS = 0x7
      N1P95_KSPS = 0x8
      N1P3_KSPS = 0x9
      N0P98_KSPS = 0xA
      N0P65_KSPS = 0xB
      N0P49_KSPS = 0xC
      N0P33_KSPS = 0xD
      N0P24_KSPS = 0xE
      N0P16_KSPS = 0xF

   def __init__(self):
      self.reset()
      self.mode = self.Mode.MANUAL

   def reset(self):
      self.write_register(self.Register.GENERAL_CFG.value, 0x1)

   def set_mode(self, mode: Mode):
      self.write_register(self.Register.SEQUENCE_CFG.value, mode.value)
      self.mode = mode

   def set_high_sampling_freq(self, freq: HighSamplingFreq):
      self.write_register(self.Register.OPMODE_CFG.value, freq.value)

   def set_low_sampling_freq(self, freq: LowSamplingFreq):
      self.write_register(self.Register.OPMODE_CFG.value, (1 << 4) | freq.value)

   def read_channel(self, ch):
      if self.mode == self.Mode.MANUAL:
         self.write_register(self.Register.CHANNEL_SEL.value, ch)
         self.read_output()
      elif self.mode == self.Mode.ON_THE_FLY:
         self.write((16+ch) << 3)

      return self.read_output()

   def dump_registers(self):
      for reg in self.Register:
         print(f'{reg}, addr: {reg.value}, value: {hex(self.read_register(reg.value))}')
   
   def dump_channels(self):
      for ch in range(0, 8):
         print(f'AIN{ch}: {self.read_channel(ch)}')

class TLA2518_FTDI(TLA2518_Base):

   def __init__(self, slave):
      self.spi = slave
      super().__init__()

   def read_register(self, addr):
      self.spi.write([RD_REG, addr, 0x00])
      return list(self.spi.read(1))[0]

   def write_register(self, addr, value):
      self.spi.write([WR_REG, addr, value])

   def set_bit(self, addr, bit):
      self.spi.write([SET_BIT, addr, bit])

   def clear_bit(self, addr, bit):
      self.spi.write([CLR_BIT, addr, bit])
      
   def read_output(self):
      l = list(self.spi.read(2))
      return (l[0] << 4) | ((l[1] & 0xF0) >> 4)

   def read_averaging_output(self):
      l = list(self.spi.read(2))
      return (l[0] << 8) | l[1]

   def write(self, value):
      self.spi.write([value])

class TLA2518(TLA2518_Base):

   def __init__(self):
      None

   def get_ftdi_backend(self, slave):
      return TLA2518_FTDI(slave) 
