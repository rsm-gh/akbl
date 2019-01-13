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
import Pyro4
import getpass
from traceback import format_exc

from AKBL.utils import print_error, print_warning
from AKBL.Paths import Paths

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

            except Exception:
                
                try:
                    #
                    # I ignore why this has to be inside an exception. Its like if there was a problem printing format_exc().
                    # The bug happens when repducing the following scenario:
                    #    1) There is a launched indicator.
                    #    2) The software is re-installed.
                    #    3) The user tries to close the indicator by usig the "Exit" button.
                    #
                    
                    if len(args) > 0:
                        print_error("Command={}, arguments=[{}]\n{}\n".format(command, ','.join((str(arg) for arg in args)), str(format_exc())))
                    else:
                        print_error("Command={}\n{}\n".format(command, str(format_exc())))
                
                except Exception:
                    pass
                
                return False
            
        else:
            print_warning("The daemon is off.")
            return False

    def reload_address(self, display_the_error=True):
        """
            It tries to make a connection with the Daemon
            and it returns True or False.
        """
        
        if not self.ping() and os.path.exists(self._paths._daemon_pyro_file):
            
            with open(self._paths._daemon_pyro_file, mode='rt', encoding='utf-8') as f:
                address = f.readline().strip()
                
            try:
                pyro = Pyro4.Proxy(address)
                pyro.ping()

                self._address = address
                self._pyro = pyro

                return True

            except Exception:
                
                if display_the_error:
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
            It checks if the Daemon is connected
            and it returns True or False.
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
            It returns the current URI of the Daemon.
        """

        return self._address

    def get_profile_names(self):
        """
            It returns a list of the existing profile names.
        """

        if not os.path.exists(self._paths._profiles_dir):
            return []

        filenames = os.listdir(self._paths._profiles_dir)
        if len(filenames) == 0:
            return []

        names = []
        for filename in filenames:
            if filename.endswith('.cfg'):
                
                path = self._paths._profiles_dir + filename

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
            
            + 'profile' is the profile name.
        """
        
        return self._command('set_profile', profile_name)

    def switch_lights(self):
        """
            Toggle on/off the lights of the keyboard.
        """
        
        return self._command('switch_lights')

    def set_lights(self, state):
        """
            Turn the lights on or off.
            
            + 'state' can be a boolean or a string
        """
        
        return self._command('set_lights', state)

    def set_colors(self, mode, speed, colors1, colors2=None):
        """
            Change the colors and the mode of the keyboard.
            
            + The available modes are: 'fixed', 'morph' and 'blink',
              'fixed' and 'blink' only take `colors1`.
                
            + Speed must be an integer. 1 =< speed >= 256
            
            + colors1 and colors2 can be a single hex_color or a list
              of hex_colors. If both arguments are used, they must
              have the same number of items.
        """
        
        return self._command('set_colors', mode, speed, colors1, colors2)
