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
        self.__pyro_address = ""
        self.__pyro_daemon = None
        self.__user = getpass.getuser()
        self.__paths = Paths(self.__user)
        self.reload_address()

    """
        General Bindings
    """

    def ping(self) -> bool:
        """Check if the Daemon is connected."""

        if self.__pyro_daemon is not None:
            try:
                self.__pyro_daemon.ping()
            except Exception:
                pass
            else:
                return True

        return False

    def get_address(self) -> str:
        """Return the current URI of the Daemon."""

        return self.__pyro_address

    def get_profiles_name(self) -> list[str]:
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

    def set_profile(self, profile_name: str) -> bool:
        """Set a profile by name."""

        profile_set = self.__command('set_profile', profile_name)

        if profile_set is None:
            profile_set = False

        return profile_set

    def switch_lights(self) -> None:
        """Switch the lights on or off."""

        return self.__command('switch_lights')

    def set_lights(self, state: bool) -> None:
        """Set the lights on or off."""

        self.__command('set_lights', state)

    def set_colors(self,
                   mode: str,
                   speed: int,
                   left_colors: str | list[str],
                   right_colors: None | str | list[str] = None) -> bool:
        """
            Change the lights colors and mode.

            :param str mode: Can be fixed, morph, or blink.
            :param int speed: Speed of the theme, 1 =< speed >= 256.
            :param str|list[str] left_colors: It can be a single hex_color or a list of hex_colors.
            :param None|str|list[str] right_colors:
                These colors are used for the morph mode.
                It can be a single hex_color or a list of hex_colors.
                It must have the same number of items than left_colors.
            :rtype: None in case of an error.
            :rtype: Bool
        """

        status = self.__command('set_colors', mode, speed, left_colors, right_colors)

        if status is None:
            status = False

        return status

    def get_computer_name(self) -> str:
        """Get the computer name set by AKBL."""

        name = self.__command('get_computer_name')
        if name is None:
            name = ""

        return name

    """
        Admin bindings.
    """

    def reload_configurations(self) -> None:
        """Reload the configurations for the current user."""
        self.__command('reload_configurations')

    def reload_address(self, verbose=True) -> bool:
        """
            Reload the pyro address, and try to make a connection with the Daemon.

            :param bool verbose: Add additional information in case of an error.
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
                self.__pyro_address = address
                self.__pyro_daemon = pyro

                return True

        self.__pyro_address = ""
        self.__pyro_daemon = None
        return False

    def connect_indicator(self, uri: str) -> None:
        """Connect the Daemon with the Indicator."""
        self.__command('connect_indicator', uri)

    def update_indicator(self) -> None:
        """Update the status (lights on/off) of the indicator."""
        self.__command('update_indicator')

    def disconnect_indicator(self) -> None:
        """Disconnect the Daemon from the Indicator."""
        self.__command('disconnect_indicator')

    """
        Private methods
    """

    def __command(self, command: str, *args):
        """Send a command to the daemon."""
        if command in ('set_profile', 'set_lights', 'switch_lights', 'reload_configurations'):
            args = [self.__user] + list(args)

        if self.__pyro_address == "":
            self.reload_address()

        if self.__pyro_address != "" and self.__pyro_daemon is not None:

            try:
                return getattr(self.__pyro_daemon, command)(*args)

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
