#!/usr/bin/python3
#

#  Copyright (C) 2015-2024 Rafael Senties Martinelli.
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

"""
    You must be very careful with this API because it runs as admin.
    The 'user' sender parameter can be faked. Currently, any user can hack this API
        and "os.utime()" any file of the system.
"""

import os
import sys
from traceback import format_exc

import Pyro4

from AKBL.Paths import Paths
from AKBL.CCParser import CCParser
from AKBL.Bindings import Bindings
from AKBL.settings import IndicatorCodes
from AKBL.utils import string_is_hex_color
from AKBL.Engine.Controller import Controller
from AKBL.Theme import factory as theme_factory
import AKBL.Computer.factory as computer_factory
from AKBL.console_printer import print_warning, print_error, print_info, print_debug


class Daemon:

    def __init__(self, fake=False):

        self.__fake = fake
        self.__computer = computer_factory.get_default_computer()

        if self.__computer is None:
            print_error("Error, no computer configuration is installed.")
            exit(1)

        print_info("Starting the computer configuration '{}'.".format(self.__computer.name))

        self.__controller = Controller(self.__computer, fake=fake)

        #                                  Save, BLock
        self.__computer_blocks_to_save = ((True, self.__computer.block_load_on_boot),
                                          (False, self.__computer.block_load_on_boot))

        # (True, self.__computer.BLOCK_STANDBY),
        # (True, self.__computer.block_ac_power),
        # (#True, self.__computer.block_charging),
        # (True, self.__computer.block_battery_sleeping),
        # (True, self.__computer.block_battery_power),
        # (True, self.__computer.block_battery_critical),

        self.__user = 'root'
        self.__paths = Paths(self.__user)
        self.__ccp = CCParser(self.__paths._configuration_file, 'GUI Configuration')

        self.__theme = None
        self.__lights_state = False
        self.__pyro_indicator = None
        self.reload_themes(self.__user)

    """
        General Bindings
    """

    @Pyro4.expose
    def ping(self, sender: str = "Anonymous") -> bool:
        """Check if the Daemon ready to execute commands."""
        print_debug()
        print_debug(sender, direct_output=True)

        if self.__fake:
            return True

        return self.__controller.is_ready()

    @Pyro4.expose
    def reload_themes(self,
                      user: str,
                      indicator: bool = True,
                      set_default: bool = True) -> None:

        print_debug(f"user={user}, indicator={indicator}, set_default={set_default}")

        if user != self.__user:
            self.__user = user
            self.__paths = Paths(user)
            self.__ccp.set_configuration_path(self.__paths._configuration_file)

        theme_factory.load_themes(self.__computer, self.__paths._profiles_dir)
        user_themes = list(theme_factory._AVAILABLE_THEMES.keys())
        print_debug(f"user={self.__user}, themes={user_themes}", direct_output=True)

        if set_default:
            _, theme_name = theme_factory.get_last_theme()
            self.__theme = theme_factory.get_theme_by_name(theme_name)
            print_debug(f"default theme={self.__theme.name}", direct_output=True)

        if self.__pyro_indicator is not None and indicator:
            try:
                self.__pyro_indicator.load_themes(user_themes,
                                                  self.__theme.name,
                                                  self.__lights_state)
            except Exception:
                print_error(format_exc())

    """
        Bindings for the users
    """

    @Pyro4.expose
    def switch_lights(self, user: str):
        """Toggle on/off the lights of the keyboard."""
        print_debug(f"user={user}")
        self.set_lights(user, not self.__lights_state)

    @Pyro4.expose
    def set_theme(self, user: str, theme_name: str) -> bool:
        """Set a theme by name."""

        print_debug(f"user={user} theme_name={theme_name}")

        if user != self.__user:
            self.__user = user
            self.__paths = Paths(user)

        self.reload_themes(user, indicator=False, set_default=False)

        if theme_name not in theme_factory._AVAILABLE_THEMES.keys():
            print_warning("The theme is not in the user list.")
            return False

        self.__theme = theme_factory._AVAILABLE_THEMES[theme_name]
        self.__illuminate_keyboard()
        return True

    @Pyro4.expose
    def set_lights(self, user: str, state: bool) -> None:
        """Set the lights on or off."""

        print_debug(f"user={user} state={state}")

        if user != self.__user:
            self.reload_themes(user)

        if state is False:

            areas_to_keep_on = self.__ccp.get_str_defval('areas_to_keep_on', '')

            if areas_to_keep_on == '':

                self.__controller.clear_constructor()

                for save, block in self.__computer_blocks_to_save:
                    self.__controller.add_block_line(save, block)
                    self.__controller.add_reset_line(self.__computer.reset_all_lights_off)

                self.__controller.apply_config()
            else:
                #
                # To turn off the lights but let some areas on, instead of sending
                # the command "all the lights off", some areas are set to black color.
                #

                areas_to_keep_on = areas_to_keep_on.split('|')

                self.__controller.clear_constructor()
                for save, block in self.__computer_blocks_to_save:

                    self.__controller.add_block_line(save, block)
                    self.__controller.add_reset_line(self.__computer.reset_all_lights_on)
                    self.__controller.add_speed_line(1)

                    for area in self.__theme.get_areas():
                        if area.name not in areas_to_keep_on:
                            for zone in area.get_zones():
                                self.__controller.add_color_line(zone.get_hex_id(), 'fixed', '#000000', '#000000')
                            self.__controller.end_colors_line()
                    self.__controller.end_block_line()
                self.__controller.apply_config()

            self.__lights_state = False
            self.__indicator_send_code(IndicatorCodes._lights_off)
        else:
            self.__illuminate_keyboard()

    @Pyro4.expose
    def set_colors(self,
                   mode: str,
                   speed: int,
                   left_colors: list[str],
                   right_colors: None | list[str] = None) -> bool:
        """
            Change the colors and the mode of the keyboard.

            :param str mode: Can be fixed, morph, or blink.
            :param int speed: Speed of the theme, 1 =< speed >= 256.
            :param list[str] left_colors: A list of hex_colors.
            :param None|list[str] right_colors:
                It will be used only of the modes are 'morph' or 'fixed'.
                It must be a list of hex_colors, with the same length as left_colors.


            #TODO: Check why right_colors is in blink mode?
        """

        print_debug(f"mode={mode} speed={speed} left_colors={left_colors} right_colors={right_colors}")

        #
        # Args checks
        #
        if mode not in ('fixed', 'morph', 'blink'):
            print_warning("Wrong mode" + str(mode))
            return False
        elif not isinstance(speed, int):
            print_warning("The speed argument must be an integer.")
            return False
        elif speed > 255:
            print_warning("The speed argument exceeds the limit > 255.")
            return False
        elif speed < 1:
            print_warning("The speed argument must be >= 1.")
            return False
        elif not isinstance(left_colors, list):
            print_warning("left_colors is not a list.")
            return False
        elif len(left_colors) == 0:
            print_warning("left_colors can not be empty.")
            return False

        if right_colors is None:
            right_colors = left_colors

        elif not isinstance(right_colors, list):
            print_warning("right_colors is not a list.")
            return False

        elif len(left_colors) != len(right_colors):
            print_warning("The colors lists must have the same length.")
            return False

        for color_list in (left_colors, right_colors):
            for color in color_list:
                if not string_is_hex_color(color):
                    print_warning(f"The colors argument must only contain hex colors. The color={color} is not valid.")
                    return False

        #
        # Set the mode
        #
        self.__controller.clear_constructor()

        for save, block in self.__computer_blocks_to_save:

            self.__controller.add_block_line(save, block)
            self.__controller.add_reset_line(self.__computer.reset_all_lights_on)
            self.__controller.add_speed_line(speed)

            for region in self.__computer.get_regions():
                for i, (left_color, right_color) in enumerate(zip(left_colors, right_colors)):

                    if i + 1 > region.max_commands:
                        print_warning(f"The number of maximum commands for the region={region.name} have been exceed. The loop was stopped at {i+1}.")
                        break

                    if mode == 'blink':
                        if region.can_blink:
                            self.__controller.add_color_line(region.hex_id, 'blink', left_color, right_color)
                        else:
                            self.__controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning(f"The mode=blink is not supported for the region={region.name}, the mode=fixed will be used instead.")

                    elif mode == 'morph':
                        if region.can_morph:
                            self.__controller.add_color_line(region.hex_id, 'morph', left_color, right_color)
                        else:
                            self.__controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning(f"The mode=morph is not supported for the region={region.name}, the mode=fixed will be used instead.")

                    else:
                        self.__controller.add_color_line(region.hex_id, 'fixed', left_color)

                self.__controller.end_colors_line()

            self.__controller.end_block_line()

        self.__controller.apply_config()

        self.__lights_state = True
        return True

    """
        Bindings for the graphical interphase
    """

    @Pyro4.expose
    def get_computer_name(self) -> str:
        print_debug()

        if self.__computer is None:
            return ""

        return self.__computer.name

    @Pyro4.expose
    def get_computer_info(self) -> tuple[str, str, str, str]:
        """
            :rtype: tuple(str: computer name,
                          str: vendor id,
                          str: product id,
                          str: device information)
        """
        print_debug()

        if self.__computer is None:
            return "", "", "", ""

        return (self.__computer.name,
                self.__computer.vendor_id,
                self.__computer.product_id,
                self.__controller.get_device_information())

    """
        Indicator Bindings
    """

    @Pyro4.expose
    def connect_indicator(self, user: str, uri: str) -> None:
        """Connect the Daemon to the Indicator."""

        print_debug("uri: {}".format(uri))

        try:
            self.__pyro_indicator = Pyro4.Proxy(uri)
        except Exception:
            self.__pyro_indicator = None
            print_warning("Failed to initialize the indicator")
            print_warning(format_exc(), direct_output=True)
        else:
            self.reload_themes(user, indicator=True)

    @Pyro4.expose
    def update_indicator(self) -> None:
        """Update the status (lights on/off) of the indicator."""

        print_debug(f"lights state={self.__lights_state}")

        if self.__lights_state:
            self.__indicator_send_code(IndicatorCodes._lights_on)
        else:
            self.__indicator_send_code(IndicatorCodes._lights_off)

    @Pyro4.expose
    def disconnect_indicator(self) -> None:
        """Disconnect the Daemon from the Indicator."""
        print_debug()
        self.__pyro_indicator = None

    """
        Private Methods
    """

    def __illuminate_keyboard(self) -> None:

        print_debug()

        # Illuminate the computer lights
        #
        print_debug("Sending commands to the controller...", direct_output=True)

        self.__controller.clear_constructor()
        for save, block in self.__computer_blocks_to_save:

            self.__controller.add_block_line(save=save, block=block)
            self.__controller.add_reset_line(self.__computer.reset_all_lights_on)
            self.__controller.add_speed_line(self.__theme.get_speed())

            for area in self.__theme.get_areas():
                for zone in area.get_zones():
                    self.__controller.add_color_line(zone.get_hex_id(),
                                                     zone.get_mode(),
                                                     zone.get_left_color(),
                                                     zone.get_right_color())

                self.__controller.end_colors_line()

            self.__controller.end_block_line()

        self.__controller.apply_config()

        #
        # Mark the current theme as "last used"
        #
        if os.path.exists(self.__theme.path):
            print_debug(f"Mark theme as last used... path={self.__theme.path}", direct_output=True)
            os.utime(self.__theme.path, None)

        # Update the Indicator
        #
        if self.__pyro_indicator is not None:
            print_debug("Sending update to the indicator...", direct_output=True)
            self.__indicator_send_code(IndicatorCodes._lights_on)
            try:
                self.__pyro_indicator.load_themes(theme_factory._AVAILABLE_THEMES.keys(),
                                                  self.__theme.name,
                                                  self.__lights_state)
            except Exception:
                print_error(format_exc())

        # Update the Daemon variables
        #
        self.__lights_state = True

    def __indicator_send_code(self, code: int) -> None:

        print_debug(f"code={code}")

        if self.__pyro_indicator is not None:
            try:
                self.__pyro_indicator.set_code(code)
            except Exception:
                print_error(format_exc())


def main(fake=False):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # todo: why is this necessary?

    akbl_daemon = Daemon(fake=fake)
    pyro_daemon = Pyro4.Daemon()
    pyro_uri = str(pyro_daemon.register(akbl_daemon))
    pyro_uri_file = Paths()._daemon_pyro_file
    print_info(f'Registering URI={pyro_uri}\nUpdating {pyro_uri_file}')
    with open(pyro_uri_file, encoding='utf-8', mode='wt') as f:
        f.write(pyro_uri)

    pyro_daemon.requestLoop()


if __name__ == "__main__":

    AKBL = Bindings(sender="Daemon")
    if AKBL.ping():
        print("Error: The Daemon is already running.")
        sys.exit(1)

    main(fake="--fake" in sys.argv)
