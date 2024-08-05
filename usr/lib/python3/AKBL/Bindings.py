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
from typing import Tuple
from traceback import format_exc

from AKBL.Paths import Paths
from AKBL.console import print_error, print_warning


class Bindings:

    def __init__(self, sender: str = "Bindings"):

        self.__sender = sender
        self.__pyro_address = ""
        self.__pyro_daemon = None
        self.__user = getpass.getuser()
        self.__paths = Paths(self.__user)
        self.reload_address()

    """
        General Bindings
    """

    def ping(self) -> bool:
        """Check if the Daemon is connected and ready to execute commands."""

        try:
            return self.__pyro_daemon.ping(sender=self.__sender + ":" + self.__pyro_address)
        except Exception:
            return False

    def get_address(self) -> str:
        """Return the current URI of the Daemon."""

        return self.__pyro_address

    def get_themes_name(self) -> list[str]:
        """Return a list of the existing user themes."""

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

    def set_theme(self, theme_name: str) -> bool:
        """Set a theme by name."""

        status = self.__command('set_theme', theme_name)
        if status is None:
            status = False

        return status

    def switch_lights(self) -> None:
        """Switch the lights on or off."""

        return self.__command('switch_lights')

    def set_lights(self, state: bool) -> None:
        """Set the lights on or off."""

        self.__command('set_lights', state)

    def set_fixed_mode(self, colors: list[str], speed: int = 1) -> bool:
        """
            Change all the light zones, with the fixed mode. Each color of the list will
            be set in all the zones, and it will move to the next value depending on the speed.

            If only one color is provided, the lights will remain at one single color and the speed
            will not have any effect.

            :param list[str] colors: A list of Hex colors.
            :param int speed: Speed for switching each zone to the next color, 1 =< speed >= 256.
        """

        if len(colors) == 0:
            raise ValueError("The list of colors can not be empty.")

        status = self.__command('set_colors', 'fixed', speed, colors, None)
        if status is None:
            status = False
        return status

    def set_blink_mode(self, colors: list[str], speed: int = 50) -> bool:
        """
            Change all the light zones, with the blink mode. Each color of the list will
            be set in all the zones, and it will blink depending on the speed.

            :param list[str] colors: A list of Hex colors.
            :param int speed: Speed for blinking, 1 =< speed >= 256.
        """

        if len(colors) == 0:
            raise ValueError("The list of colors can not be empty.")

        status = self.__command('set_colors', 'blink', speed, colors, None)
        if status is None:
            status = False
        return status

    def set_morph_mode(self,
                       colors: list[Tuple[str, str]],
                       speed: int = 50) -> bool:
        """
            Change all the light zones, with the morph mode. Each color pair of the list will
            be set in all the zones, and it will create a gradient from the first color, to
            the second color, depending on the speed.

            :param list[tuple(str, str)] colors: A list of lists containing two values of Hex colors.
            :param int speed: Speed for switching each zone to the next color, 1 =< speed >= 256.
        """

        if len(colors) == 0:
            raise ValueError("The list of colors can not be empty.")

        left_colors = []
        right_colors = []

        for left_color, right_color in colors:
            left_colors.append(left_color)
            right_colors.append(right_color)

        status = self.__command('set_colors', "morph", speed, left_colors, right_colors)

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

    def reload_address(self, verbose=False) -> bool:
        """Reload the pyro address, and try to make a connection with the Daemon."""

        if not self.ping() and os.path.exists(self.__paths._daemon_pyro_file):

            with open(self.__paths._daemon_pyro_file, mode='rt', encoding='utf-8') as f:
                address = f.readline().strip()

            try:
                pyro = Pyro4.Proxy(address)
                pyro.ping(sender=self.__sender + ":" + self.__pyro_address)

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
        if command in ('set_theme', 'set_lights', 'switch_lights', 'reload_configurations', 'connect_indicator'):
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
