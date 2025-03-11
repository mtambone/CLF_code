#!/usr/bin/env python3
# coding=utf-8

import argparse
import os
import time
import sys
import cmd2
import functools
import getpass
import numpy as np
from cmd2.table_creator import (
    Column,
    SimpleTable,
    HorizontalAlignment
)
from typing import (
    List,
)

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.RPC import RPCDevice
from lib.Centurion import Centurion

class CLF_app(cmd2.Cmd):

    def __init__(self, mode, param):
        super().__init__(allow_cli_args=False)
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_macro
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_shell
        del cmd2.Cmd.do_shortcuts

        self.param = param
        self.port = self.param.port

        #self.prompt = self.bright_black(f'CLF:{self.param.mode} > ')

            # Move text styles here
        self.bright_black = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_black)
        self.bright_yellow = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_yellow)
        self.bright_green = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_green)
        self.bright_red = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_red)
        self.bright_cyan = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_cyan)
        self.bright_blue = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_blue)
        self.yellow = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.yellow)
        self.blue = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_blue)
        self.alarm_red = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_white, bg=cmd2.ansi.bg.bright_red)

        self.allow_style = cmd2.ansi.allow_style
        self.prompt = self.bright_black(f'CLF: > ')

        cmd2.categorize(
            (cmd2.Cmd.do_alias, cmd2.Cmd.do_help, cmd2.Cmd.do_history, cmd2.Cmd.do_quit, cmd2.Cmd.do_set, cmd2.Cmd.do_run_script),
            "General commands" 
        )
        
        def ansi_print(self, text):
            cmd2.ansi.style_aware_write(sys.stdout, text + '\n')

            # # Text styles used in the data
            # bright_black = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_black)
            # bright_yellow = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_yellow)
            # bright_green = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_green)
            # bright_red = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_red)
            # bright_cyan= functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_cyan)
            # bright_blue = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_blue)
            # yellow = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.yellow)
            # blue = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_blue)
            # alarm_red = functools.partial(cmd2.ansi.style, fg=cmd2.ansi.fg.bright_white, bg=cmd2.ansi.bg.bright_red)

            columns: List[Column] = list()
            columns.append(Column("", width=2))
            columns.append(Column("", width=6, data_horiz_align=HorizontalAlignment.CENTER))
            columns.append(Column("", width=5, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=9, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=7, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=7, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=12, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=20, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=13, data_horiz_align=HorizontalAlignment.RIGHT))
            columns.append(Column("", width=14, data_horiz_align=HorizontalAlignment.CENTER))

            st = SimpleTable(columns, divider_char=None)

    rpc = RPCDevice('/dev/ttyr00')  # Modifica la porta se necessario
    laser = Centurion("/dev/ttyr01")
    laser.connect()
    
    ########add functions##############

    ##### RPC Functions ############
    rpc_parser = argparse.ArgumentParser()
    rpc_parser.add_argument('value', type=int, help='number of plug 1-6 (RPC_RAMAN = 1 RPC_RAD = 2 RPC_LSR = 3 RPC_RCOVER = 4 RPC_VCOVER = 5 RPC_VXM = 6)')
    rpc_parser.add_argument('status', type=int, help='status of the plug 1=ON 0=OFF')

    @cmd2.with_argparser(rpc_parser)
    @cmd2.with_category("Instruments command")
    def do_rpc(self, args: argparse.Namespace) -> None:
        if args.status == 1:
            print('on to plug ' + str(args.value))
            comando ='on ' + str(args.value)
        else:
            print('off to plug ' + str(args.value) )
            comando ='off ' + str(args.value)
        self.rpc.send_command(comando)
    
    ######### LASER FUNCTIONS ##################
    @cmd2.with_category("laser command")
    def do_lsr_init(self, args: argparse.Namespace) -> None:
        self.laser.set_mode(100, 1, 1, 1, 1, 1, dpw = 140, qsdelay = 145)

    @cmd2.with_category("laser command")
    def do_lsr_fire(self, args: argparse.Namespace) -> None:
        self.laser.fire()

    lsr_energy_parser = argparse.ArgumentParser()
    lsr_energy_parser.add_argument('value', type=int, help='energy of the laser shot in us')
    @cmd2.with_argparser(lsr_energy_parser)
    @cmd2.with_category("laser command")
    def do_lsr_energy(self, args: argparse.Namespace) -> None:
        self.laser.set_pwdth(args.value)
    
    @cmd2.with_category("laser command")
    def do_lsr_checktemps(self, args: argparse.Namespace) -> None:
        self.laser.check_temps()


        

        
if __name__ == '__main__':
   parser = argparse.ArgumentParser()
   parser.add_argument('--mode', default='rtu', const='rtu', nargs='?', choices=['rtu', 'tcp'], help='set modbus interface (default: %(default)s)')
   parser.add_argument('--port', action='store', type=str, help='serial port device (default: /dev/ttyPS2)', default='/dev/ttyPS2')
   parser.add_argument('--host', action='store', type=str, help='mbusd hostname (default: localhost)', default='localhost')
   args = parser.parse_args()

   app = CLF_app(args.mode,args)
   app.cmdloop()

