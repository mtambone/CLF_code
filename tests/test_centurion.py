#!/usr/bin/env python3

import sys
import os
import time

lib_path = os.path.abspath('opt/CLF_CODE/lib/')

# Append it to sys.path
sys.path.append(lib_path)


from Centurion import Centurion

c = Centurion("/dev/ttyr00")
time.sleep(1)
c.set_mode()
time.sleep(5)
c.warmup()
c.read_bytes()
