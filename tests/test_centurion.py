#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.Centurion import Centurion

c = Centurion("/dev/ttyr00")
