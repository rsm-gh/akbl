#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
#
#  AKBL is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License 3 as published by
#   the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
    This module prints directly to the user. console_printer should not be used !
"""


import sys

from AKBL.Texts import Texts
from AKBL.Bindings import Bindings
from AKBL.settings import __version__


def process_args(args):
    if len(args) < 2:
        print(Texts.Commands._wrong_argument)
        return

    akbl_bindings = Bindings(sender="CMD")
    arg1 = str(args[1])

    match arg1:
        case '--help' | '-h':
            print(Texts.Commands._help)

        case '--license' | '-l':
            print(Texts.Commands._license)

        case '--version' | '-v':
            print(__version__)

        case '--ping':
            print(akbl_bindings.ping())

        case '--off' | '--on' | '--switch' | '--set-theme':

            if not akbl_bindings.ping():
                print(Texts.Commands._daemon_off)
                return

            match arg1:
                case '--off':
                    akbl_bindings.set_lights(False)

                case '--on':
                    akbl_bindings.set_lights(True)

                case '--switch':
                    akbl_bindings.switch_lights()

                case '--set-theme':
                    if len(args) != 3:
                        print(Texts.Commands._wrong_argument)
                    else:
                        akbl_bindings.set_theme(args[2])
                case _:
                    print(Texts.Commands._wrong_argument)

        case _:
            print(Texts.Commands._wrong_argument)


if __name__ == '__main__':
    process_args(sys.argv)
