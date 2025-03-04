#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.FPGARunControl import FPGARunControl
from datetime import datetime
import time


rc = FPGARunControl("COM13")
rc.connect()


##### method to read internal pps counter #######
def read_PPS_counter():
      temp=0
      temp=rc.read_register(0)
      temp_H=0
      temp_H=rc.read_register(1)
      return ((temp_H<<16)+temp)

#print(read_PPS_counter())

### method to align pps counter to unix time from pc ##########
def align_unix_time():
      timeout = int(time.time()) + 1.5
      while True:
        ts = time.time()
        if ts > timeout:
            unix_time = int(ts)#int(time.time())
            rc.write_register(25, unix_time & 0xFFFF) 
            time.sleep(0.1)
            rc.write_register(26, (unix_time >> 16)& 0xFFFF)
            break

#align_unix_time()

def set_laser_frequency(freq):
     periodo =int((1/freq)*100_000_000)
     rc.write_register(27, periodo & 0xFFFF)
     time.sleep(0.1)
     rc.write_register(28, (periodo >> 16)& 0xFFFF)


set_laser_frequency(10)

def set_laser_shots(shots):
     if shots < 65535:
      rc.write_register(4, shots)
     else:
      rc.write_register(4, 65535) 
      print('Maximum 65535 shots, update will come soon')

set_laser_shots(100)

def set_laser_energy_us(delay_us):
     var=(delay_us*100)
     rc.write_register(14, var & 0xFFFF)
     time.sleep(0.1)
     rc.write_register(15, (var >> 16)& 0xFFFF)

set_laser_energy_us(140)


rc.write_register(3, 3)
