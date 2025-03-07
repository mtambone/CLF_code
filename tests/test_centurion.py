#!/usr/bin/env python3

import sys
import os
import time

lib_path = os.path.abspath('/home/tambone/Desktop/Matteo/CLF_code/lib')

# Append it to sys.path
sys.path.append(lib_path)


from Centurion import Centurion

c = Centurion("/dev/ttyr00")
time.sleep(1)
c.read_bytes()
