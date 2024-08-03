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
from AKBL.console import print_error, print_warning


class Bindings:

    def __init__(self):
        self.__address = None
        self.__pyro = None
        self.__user = getpass.getuser()
        self.__paths = Paths(self.__user)
        self.reload_address()

    """
        General Bindings
    """

    def ping(self) -> bool:
        """Check if the Daemon is connected."""

        if self.__pyro is not None:
            try:
                self.__pyro.ping()
            except Exception:
                pass
            else:
                return True

        return False

    def get_address(self) -> str | None:
        """
            Return the current URI of the Daemon.

            :rtype: None if the Daemon is not connected.
            :rtype: Str if the Daemon is/was connected.
        """

        return self.__address

    def get_profile_names(self) -> list[str]:
        """Return a list of the existing profile names."""

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

    def set_profile(self, profile_name: str) -> None | bool:
        """
            Activate a profile.
            
            :param str profile_name: Is the profile to be set.
            :rtype: None in case of an error.
            :rtype: Bool
        """

        return self.__command('set_profile', profile_name)

    def switch_lights(self) -> None:
        """Toggle on/off the lights of the keyboard."""

        return self.__command('switch_lights')

    def set_lights(self, state: bool | str) -> None:
        """
            Turn the lights on or off.
            
            :param bool|str state: Status to be set.
            :rtype: None
        """

        return self.__command('set_lights', state)

    def set_colors(self,
                   mode: str,
                   speed: int,
                   left_colors: str | list[str],
                   right_colors: None | str | list[str] = None) -> None | bool:
        """
            Change the colors and the mode of the keyboard.

            :param str mode: Can be fixed, morph, or blink.
            :param int speed: Speed of the theme, 1 =< speed >= 256.
            :param str|list[str] left_colors: It can be a single hex_color or a list of hex_colors.
            :param None|str|list[str] right_colors: It can be a single hex_color or a list of hex_colors.
            If used, it must have the same number of items than left_colors.
            :rtype: None in case of an error.
            :rtype: Bool
        """

        return self.__command('set_colors', mode, speed, left_colors, right_colors)

    def get_computer_name(self) -> None | str:
        """
            Get the computer name set by AKBL.

            :rtype: None in case of an error.
            :rtype: Str
        """
        return self.__command('get_computer_name')

    """
        Admin bindings.
    """

    def reload_configurations(self) -> None:
        """
            Reload the configurations for the current user.

            :rtype: None
        """
        return self.__command('reload_configurations')

    def reload_address(self, verbose=True) -> bool:
        """
            Try to make a connection with the Daemon.

            :param bool verbose: Add additional information in case of an error.
            :rtype: Bool
        """

        if not self.ping() and os.path.exists(self.__paths._daemon_pyro_file):

            with open(self.__paths._daemon_pyro_file, mode='rt', encoding='utf-8') as f:
                address = f.readline().strip()

            try:
                pyro = Pyro4.Proxy(address)
                pyro.ping()

            except Exception:
                if verbose:
                    print_error(format_exc())
            else:
                self.__address = address
                self.__pyro = pyro

                return True

        self.__address = None
        self.__pyro = None
        return False

    def connect_indicator(self, uri: str) -> None:
        """Connect the Daemon with the Indicator."""
        return self.__command('connect_indicator', uri)

    def update_indicator(self) -> None:
        """Update the status lights on/off of the indicator."""
        return self.__command('update_indicator')

    def disconnect_indicator(self) -> None:
        """Disconnect the Daemon from the Indicator."""
        return self.__command('disconnect_indicator')

    """
        Private methods
    """

    def __command(self, command: str, *args):
        """Send a command to the daemon."""
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
                    # I ignore why this has to be inside an exception.
                    # Its like if there was a problem printing format_exc().
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
