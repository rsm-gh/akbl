#!/usr/bin/python3
#

#  Copyright (C) 2014-2016, 2018  Rafael Senties Martinelli 
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
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.

import sys
import os

from AKBL.texts import TEXT_ERROR_DAEMON_OFF, TEXT_HELP, TEXT_LICENSE, TEXT_WRONG_ARGUMENT
from AKBL.Bindings import Bindings
from AKBL.Configuration.Paths import Paths


AKBLConnection = Bindings()
PATHS = Paths()


def send_command(command, *args):
    if not os.path.exists(PATHS.SYSTEMCTL_PATH) or not AKBLConnection.ping():
        print(TEXT_ERROR_DAEMON_OFF)
    else:
        AKBLConnection._command(command, *args)

if __name__ == '__main__':

    total = len(sys.argv)

    if total >= 2:
        arg1 = str(sys.argv[1])

        if arg1 == '--help' or arg1 == '-h':
            print(TEXT_HELP)

        elif arg1 == '--license' or arg1 == '-l':
            print(TEXT_LICENSE)

        elif arg1 == '--daemon-is-on':
            print(AKBLConnection.ping())

        elif arg1 in ('--off', '--on', '--change', '--set-profile') and not AKBLConnection.ping():
            print(TEXT_ERROR_DAEMON_OFF)

        elif arg1 == '--off':
            send_command('set_lights', False)
        
        elif arg1 == '--on':
            send_command('set_lights', True)
        
        elif arg1 == '--change':
            send_command('switch_lights')
            
        elif arg1 == '--set-profile':
            send_command('set_profile', sys.argv[2])
        else:
            print(TEXT_WRONG_ARGUMENT)
    else:
        print(TEXT_WRONG_ARGUMENT)
