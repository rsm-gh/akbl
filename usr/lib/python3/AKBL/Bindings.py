#!/usr/bin/python3
#

#  Copyright (C) 2015-2016, 2018-2019, 2024 Rafael Senties Martinelli.
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


import os
import Pyro4
import getpass
from traceback import format_exc

from AKBL.Paths import Paths
from AKBL.utils import print_error, print_warning

class Bindings:

    def __init__(self):
        self.__address = None
        self.__pyro = None
        self.__user = getpass.getuser()
        self.__paths = Paths(self.__user)
        self.reload_address()

    def __command(self, command, *args):
        """
            Send a command to the daemon and return a tuple containing (boolean, response).
            The boolean indicates if the command was successful or not.
            The response contains the information returned by the command.
        """
        if command in ('set_profile', 'set_lights', 'switch_lights', 'reload_configurations'):
            args = [self.__user] + list(args)

        if self.__address is None:
            self.reload_address()

        if self.__address is not None and self.__pyro is not None:

            try:
                return getattr(self.__pyro, command)(*args)

            except Exception:

                try:
                    #
                    # I ignore why this has to be inside an exception. Its like if there was a problem printing format_exc().
                    # The bug happens when reducing the following scenario:
                    #    1) There is a launched indicator.
                    #    2) The software is re-installed.
                    #    3) The user tries to close the indicator by using the "Exit" button.
                    #

                    if len(args) > 0:
                        print_error(
                            "Command={}, arguments=[{}]\n{}\n".format(command, ','.join((str(arg) for arg in args)),
                                                                      str(format_exc())))
                    else:
                        print_error("Command={}\n{}\n".format(command, str(format_exc())))

                except Exception:
                    print_error("NO TRACEBACK: Command={}\n".format(command))
        else:
            print_warning("The daemon is off.")

        return None

    def ping(self):
        """
            Check if the Daemon is connected and return `True` or `False`.
        """

        if self.__pyro is not None:
            try:
                self.__pyro.ping()
            except Exception:
                pass
            else:
                return True

        return False

    def get_address(self):
        """
            Returns the current URI of the Daemon.
        """

        return self.__address

    def get_profile_names(self):
        """
            Return a list of the existing profile names.
        """

        if not os.path.exists(self.__paths._profiles_dir):
            return []

        filenames = os.listdir(self.__paths._profiles_dir)
        if len(filenames) == 0:
            return []

        names = []
        for filename in filenames:
            if filename.endswith('.cfg'):

                path = self.__paths._profiles_dir + filename

                with open(path, mode='rt', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    variables = line.strip().split('=')
                    if len(variables) == 2:
                        var_name = variables[0]
                        var_arg = variables[1]
                        if var_name == 'name':
                            if var_arg == '':
                                name = os.path.basename(path)
                            else:
                                name = var_arg

                            if name.endswith('.cfg'):
                                name = name[:-4]

                            names.append(name)
                            break

        names.sort()

        return names

    def set_profile(self, profile_name):
        """
            Set a profile from the existing profiles.
            
            + 'Profile' is the profile name.
        """

        return self.__command('set_profile', profile_name)

    def switch_lights(self):
        """
            Toggle on/off the lights of the keyboard.
        """

        return self.__command('switch_lights')

    def set_lights(self, state):
        """
            Turn the lights on or off.
            
            + 'state' can be a boolean or a string
        """

        return self.__command('set_lights', state)

    def set_colors(self, mode, speed, colors1, colors2=None):
        """
            Change the colors and the mode of the keyboard.
            
            + The available modes are: 'fixed', 'morph' and 'blink',
              'fixed' and 'blink' only take `colors1`.
                
            + Speed must be an integer. 1 =< speed >= 256
            
            + Colors1 and colors2 can be a single hex_color or a list
              of hex_colors. If both arguments are used, they must
              have the same number of items.
        """

        return self.__command('set_colors', mode, speed, colors1, colors2)

    def get_computer_name(self):
        return self.__command('get_computer_name')

    """
        Admin bindings.
    """

    def reload_configurations(self):
        return self.__command('reload_configurations')

    def reload_address(self, display_the_error=True):
        """
            It tries to make a connection with the Daemon, and it returns True or False.
        """

        if not self.ping() and os.path.exists(self.__paths._daemon_pyro_file):

            with open(self.__paths._daemon_pyro_file, mode='rt', encoding='utf-8') as f:
                address = f.readline().strip()

            try:
                pyro = Pyro4.Proxy(address)
                pyro.ping()

            except Exception:
                if display_the_error:
                    print_error(format_exc())
            else:
                self.__address = address
                self.__pyro = pyro

                return True

        self.__address = None
        self.__pyro = None
        return False

    def indicator_start(self, uri):
        return self.__command('indicator_start', uri)

    def indicator_get_state(self):
        return self.__command('indicator_get_state')

    def indicator_kill(self):
        return self.__command('indicator_kill')
