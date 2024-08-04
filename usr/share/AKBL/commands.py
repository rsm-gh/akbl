#!/usr/bin/python3
#

#  Copyright (C) 2014-2016, 2018, 2024 Rafael Senties Martinelli.
#
#  This program is free software; you can redistribute it and/or modify
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

import sys

import AKBL.texts as texts
from AKBL.Bindings import Bindings
from AKBL.settings import __version__


def process_args(args):
    if len(args) < 2:
        print(texts._TEXT_WRONG_ARGUMENT)
        return

    akbl_bindings = Bindings(sender="CMD")
    arg1 = str(args[1])

    if arg1 in ('--help', '-h'):
        print(texts._TEXT_HELP)

    elif arg1 in ('--license', '-l'):
        print(texts._TEXT_LICENSE)

    elif arg1 in ('--version', '-v'):
        print(__version__)

    elif arg1 == '--ping':
        print(akbl_bindings.ping())

    elif arg1 in ('--off', '--on', '--switch', '--set-theme'):

        if not akbl_bindings.ping():
            print(texts._TEXT_ERROR_DAEMON_OFF)

        elif arg1 == '--off':
            akbl_bindings.set_lights(False)

        elif arg1 == '--on':
            akbl_bindings.set_lights(True)

        elif arg1 == '--switch':
            akbl_bindings.switch_lights()

        elif arg1 == '--set-theme':
            if len(args) != 3:
                print(texts._TEXT_WRONG_ARGUMENT)
            else:
                akbl_bindings.set_theme(args[2])

    else:
        print(texts._TEXT_WRONG_ARGUMENT)


if __name__ == '__main__':
    process_args(sys.argv)
