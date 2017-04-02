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
import pwd

from AKBL import AKBL

# Local imports
from utils import getuser
from Configuration.Paths import Paths
from Configuration.CCParser import CCParser
from texts import TEXT_ERROR_DAEMON_OFF, TEXT_HELP, TEXT_LICENSE, TEXT_NON_LINUX_USER, TEXT_WRONG_ARGUMENT

AKBLConnection = AKBL()
PATHS = Paths()

def send_command(command, *args):
    if not os.path.exists(PATHS.SYSTEMCTL_PATH) or not AKBLConnection.ping():
        print(TEXT_ERROR_DAEMON_OFF)
    else:
        AKBLConnection._command(command, *args)


if __name__ == '__main__':

    total = len(sys.argv)

    if total >= 2:
        arg = str(sys.argv[1])

        if arg == '--help' or arg == '-h':
            print(TEXT_HELP)

        elif arg == '--license' or arg == '-l':
            print(TEXT_LICENSE)

        elif arg in ('--set-boot-user', '--get-boot-user'):
            ccp = CCParser(PATHS.GLOBAL_CONFIG, 'Global alienware-kbl Configuration')

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

        elif arg == '--daemon-is-on':
            print(AKBLConnection.ping())

        elif arg in ('--off', '--on', '--change', '--set-profile') and not AKBLConnection.ping():
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
