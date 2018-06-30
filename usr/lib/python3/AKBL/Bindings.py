#!/usr/bin/python3
#

#  Copyright (C) 2015-2016, 2018  Rafael Senties Martinelli 
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


import os
import sys
import Pyro4
import getpass
from traceback import format_exc

from AKBL.utils import print_error, print_warning
from AKBL.Configuration.Paths import Paths

class Bindings:

    def __init__(self):
        self._address = False
        self._pyro = False
        self._paths = Paths()
        self._user = getpass.getuser()
        self.reload_address()

    def _command(self, command, *args):
        """
            Send a command to the daemon and return a tuple containing (boolean, response).
            The boolean indicates weather the command was succesfull or not, and the response
            contains the information returned by the command.
        """
        if command in ('set_profile', 'set_lights', 'switch_lights', 'reload_configurations'):
            args = [self._user] + list(args)

        if not self._address:
            self.reload_address()

        if self._address:
            try:
                response = getattr(self._pyro, command)(*args)
                return response

            except Exception as e:
                print_error("Command={}, arguments=[{}]\n{}\n".format(command, ','.join((str(arg) for arg in args)), format_exc()))
                return False
        else:
            print_warning("The daemon is off.")
            return False

    def reload_address(self):
        """
            Try to make a connection with the Daemon.
            Returns True or False
        """
        if not self.ping() and os.path.exists(self._paths.DAEMON_PYRO_PATH):
            with open(self._paths.DAEMON_PYRO_PATH, mode='rt', encoding='utf-8') as f:
                address = f.readline().strip()
            try:
                pyro = Pyro4.Proxy(address)
                pyro.ping()

                self._address = address
                self._pyro = pyro

                return True

            except Exception as e:
                print_error(format_exc())

                self._address = False
                self._pyro = False
                return False
        else:
            self._address = False
            self._pyro = False
            return False

    def ping(self):
        """
            Check if the Daemon is connected.
            Returns True or False
        """
        if self._pyro:
            try:
                self._pyro.ping()
                return True
            except:
                pass

        return False

    def get_address(self):
        """
            Return the current URI of the Daemon.
        """

        return self._address

    def get_profile_names(self):
        """
            Return a list of the existing profile names.
        """

        if not os.path.exists(self._paths.PROFILES_PATH):
            return []

        filenames = os.listdir(self._paths.PROFILES_PATH)
        if len(filenames) == 0:
            return []

        names = []
        for filename in filenames:
            if filename.endswith('.cfg'):

                with open(self._paths.PROFILES_PATH + filename, mode='rt', encoding='utf-8') as f:
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

    """
        Default Daemon Commands
    """

    def set_profile(self, profile_name):
        return self._command('set_profile', profile_name)

    def switch_lights(self):
        return self._command('switch_lights')

    def set_lights(self, state):
        return self._command('set_lights', state)

    def set_colors(self, mode, speed, colors1, colors2=None):
        return self._command('set_colors', mode, speed, colors1, colors2)
