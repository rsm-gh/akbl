#!/usr/bin/python3
#

#  Copyright (C) 2014-2016  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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
from common import getuser

# local imports
from Paths import Paths
PATHS = Paths()
from Texts import *


def send_command(command, *args):
    AKBLConnection = AlienwareKBL()

    if not os.path.exists(PATHS.SYSTEMCTL_PATH) or not AKBLConnection.ping():
        print(TEXT_ERROR_DAEMON_OFF)
    else:
        AKBLConnection._command(command, *args)


if __name__ == '__main__':
    import pwd

    total = len(sys.argv)

    if total >= 2:
        arg = str(sys.argv[1])

        if arg == '--help' or arg == '-h':
            print(TEXT_HELP)

        elif arg == '-v' or arg == '--version':
            print(TEXT_VERSION)

        elif arg == '--license' or arg == '-l':
            print(TEXT_LICENSE)

        elif arg in ('--set-boot-user', '--get-boot-user'):
            from CCParser import CCParser
            ccp = CCParser(
                PATHS.GLOBAL_CONFIG,
                'Global alienware-kbl Configuration')

            if arg == '--set-boot-user':
                if getuser() == 'root':

                    boot_user = sys.argv[2]

                    # Check if the user of the configuration file exists
                    try:
                        pwd.getpwnam(boot_user)
                    except:
                        print(TEXT_NON_LINUX_USER)
                        exit()

                    ccp.write('boot_user', boot_user)
                else:
                    print(TEXT_ONLY_ROOT)
            else:
                print(ccp.get_str_defval('boot_user', 'root'))

        else:
            try:
                # This exception is used when pyro
                # is not installed.
                from AlienwareKBL import AlienwareKBL

                AKBLConnection = AlienwareKBL()

                if AKBLConnection.ping():
                    AKBL_DAEMON = True
                else:
                    AKBL_DAEMON = False
            except:
                AKBL_DAEMON = False

            if arg == '--daemon-is-on':
                print(AKBL_DAEMON)

            elif arg in ('--off', '--on', '--change', '--set-profile') and not AKBL_DAEMON:
                print(TEXT_ERROR_DAEMON_OFF)

            elif arg == '--off':
                send_command('set_lights', False)
            elif arg == '--on':
                send_command('set_lights', True)
            elif arg == '--change':
                send_command('switch_lights')
            elif arg == '--set-profile':
                send_command('set_profile', sys.argv[2])
            else:
                print(TEXT_WRONG_ARGUMENT)
    else:
        print(TEXT_WRONG_ARGUMENT)
