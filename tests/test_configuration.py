import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.Config import Configuration
from lib.Collections import MotorCollection

cfg = Configuration()
cfg.read()

# configure motors
mc = MotorCollection()
for mname, mparams in cfg.motors.items():
    port_params = cfg.get_port_params(mparams['port'])
    mc.add(mparams['id'], mname, 
           port=port_params['port'],
           speed=port_params['speed'],
           bytesize=port_params['bytesize'],
           parity=port_params['parity'],
           stopbits=port_params['stopbits'],
           timeout=port_params['timeout']
    )

print(mc)

mc.get("NorthSud").move(10)

