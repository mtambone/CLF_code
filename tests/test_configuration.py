import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.Configuration import Configuration
from lib.DeviceCollection import DeviceCollection

cfg = Configuration()
cfg.read()

dc = DeviceCollection()

# outlets
for oname, oparams in cfg.outlets.items():
    port_params = cfg.get_port_params(oparams['port'])
    dc.add_outlet(oparams['id'], oname,
           port=port_params['port'],
           speed=port_params['speed'],
           bytesize=port_params['bytesize'],
           parity=port_params['parity'],
           stopbits=port_params['stopbits'],
           timeout=port_params['timeout']
    )

# motors
for mname, mparams in cfg.motors.items():
    port_params = cfg.get_port_params(mparams['port'])
    dc.add_motor(mparams['id'], mname,
           port=port_params['port'],
           speed=port_params['speed'],
           bytesize=port_params['bytesize'],
           parity=port_params['parity'],
           stopbits=port_params['stopbits'],
           timeout=port_params['timeout']
    )

dc.get_outlet("RAMAN2").on()
dc.get_motor("Cover").move_ABS(0)
