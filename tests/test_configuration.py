import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.Configuration import Configuration
from lib.DeviceCollection import DeviceCollection

cfg = Configuration()
cfg.read()

dc = DeviceCollection()
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

dc.get_outlet("RAMAN2").on()

