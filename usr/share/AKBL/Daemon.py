#!/usr/bin/python3
#

#  Copyright (C) 2015-2018, 2024 Rafael Senties Martinelli.
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
from traceback import format_exc

from common import IndicatorCodes
from AKBL.Paths import Paths
from AKBL.CCParser import CCParser
from AKBL.utils import string_is_hex_color
from AKBL.Engine.Controller import Controller
from AKBL.Theme import factory as theme_factory
import AKBL.Computer.factory as computer_factory
from AKBL.console import print_warning, print_error, print_info, print_debug


class Daemon:

    def __init__(self):

        self.__computer = computer_factory.get_installed_computer()

        if self.__computer is None:
            print("Error, no computer configuration is installed.", flush=True)
            exit(1)

        print("Starting the computer configuration '{}'.".format(self.__computer.name), flush=True)

        self.__controller = Controller(self.__computer)

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
        self.reload_configurations(self.__user)

    """
        General Bindings
    """

    @Pyro4.expose
    def ping(self) -> None:
        print_debug()

    @Pyro4.expose
    def reload_configurations(self,
                              user: str,
                              indicator: bool = True,
                              set_default: bool = True) -> None:

        print_debug("user={} indicator={} set_default={}".format(user, indicator, set_default))

        if user != self.__user:
            self.__user = user
            self.__paths = Paths(user)
            self.__ccp.set_configuration_path(self.__paths._configuration_file)

        theme_factory.load_profiles(self.__computer, self.__paths._profiles_dir)

        if set_default:
            _, profile_name = theme_factory.get_last_configuration()
            self.__theme = theme_factory.get_theme_by_name(profile_name)

        if self.__pyro_indicator is not None and indicator:
            try:
                self.__pyro_indicator.load_profiles(theme_factory._AVAILABLE_THEMES.keys(),
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
        print_debug("user={}".format(user))
        self.set_lights(user, not self.__lights_state)

    @Pyro4.expose
    def set_profile(self, user: str, profile_name: str) -> bool:
        """
            Activate a profile.

            :param str user: Name of the user.
            :param str profile_name: Is the profile to be set.
            :rtype: None in case of an error.
            :rtype: Bool
        """

        print_debug("user={} theme_name={}".format(user, profile_name))

        if user != self.__user:
            self.__user = user
            self.__paths = Paths(user)

        self.reload_configurations(user, indicator=False, set_default=False)

        if profile_name in theme_factory._AVAILABLE_THEMES.keys():
            self.__theme = theme_factory._AVAILABLE_THEMES[profile_name]
            self.__illuminate_keyboard()
            return True

        return False

    @Pyro4.expose
    def set_lights(self, user: str, state: bool) -> None:
        """Set the lights on or off."""

        print_debug("user={} state={}".format(user, state))

        if user != self.__user:
            self.reload_configurations(user)

        if state is False:

            areas_to_keep_on = self.__ccp.get_str_defval('areas_to_keep_on', '')

            if areas_to_keep_on == '':

                self.__controller.erase_config()

                for save, block in self.__computer_blocks_to_save:
                    self.__controller.add_block_line(save, block)
                    self.__controller.add_reset_line(self.__computer.reset_all_lights_off)

                self.__controller.apply_config()
            else:
                """
                    To turn off the lights but let some areas on, instead of sending the command "all the lights off",
                    some areas are set to black color.
                """

                areas_to_keep_on = areas_to_keep_on.split('|')

                self.__controller.erase_config()
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
            self.__indicator_send_code(IndicatorCodes.lights_off)
        else:
            self.__illuminate_keyboard()

    @Pyro4.expose
    def set_colors(self,
                   mode: str,
                   speed: int,
                   left_colors: str | list[str],
                   right_colors: None | str | list[str] = None) -> bool:
        """
            Change the colors and the mode of the keyboard.

            :param str mode: Can be fixed, morph, or blink.
            :param int speed: Speed of the theme, 1 =< speed >= 256.
            :param str|list[str] left_colors: It can be a single hex_color or a list of hex_colors.
            :param None|str|list[str] right_colors: It can be a single hex_color or a list of hex_colors.
            If provided, it must have the same number of items than left_colors.
            :rtype: None in case of an error.
            :rtype: Bool
        """

        print_debug("mode={} speed={} left_colors={} right_colors={}".format(mode, speed, left_colors, right_colors))

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

        if not isinstance(left_colors, list) and not isinstance(left_colors, tuple):
            left_colors = [left_colors]

        if right_colors is None:
            right_colors = left_colors

        elif not isinstance(right_colors, list) and not isinstance(right_colors, tuple):
            right_colors = [right_colors]

        if len(left_colors) != len(right_colors):
            print_warning("The colors lists must have the same length.")
            return False

        for color_list in (left_colors, right_colors):
            for color in color_list:
                if not string_is_hex_color(color):
                    print_warning(
                        "The colors argument must only contain hex colors. The color={} is not valid.".format(color))
                    return False

        self.__controller.erase_config()

        for save, block in self.__computer_blocks_to_save:

            self.__controller.add_block_line(save, block)
            self.__controller.add_reset_line(self.__computer.reset_all_lights_on)
            self.__controller.add_speed_line(speed)

            for region in self.__computer.get_regions():
                for i, (left_color, right_color) in enumerate(zip(left_colors, right_colors)):

                    if i + 1 > region.max_commands:
                        print_warning(
                            "The number of maximum commands for the region={} have been exceed. The loop was stopped at {}.".format(
                                region.name, i + 1))
                        break

                    if mode == 'blink':
                        if region.can_blink:
                            self.__controller.add_color_line(region.hex_id, 'blink', left_color, right_color)
                        else:
                            self.__controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning(
                                "The mode=blink is not supported for the region={}, the mode=fixed will be used instead.".format(
                                    region.name))

                    elif mode == 'morph':
                        if region.can_morph:
                            self.__controller.add_color_line(region.hex_id, 'morph', left_color, right_color)
                        else:
                            self.__controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning(
                                "The mode=morph is not supported for the region={}, the mode=fixed will be used instead.".format(
                                    region.name))

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

    @Pyro4.expose
    def modify_lights_state(self, value) -> None:
        """
            This method does not change the lights of the keyboard,
            it only updates the daemon and the indicator
        """

        print_debug("value={}".format(value))

        if value in (False, 'False', 'false'):
            self.__lights_state = False
            self.__indicator_send_code(IndicatorCodes.lights_off)
        else:
            self.__lights_state = True
            self.__indicator_send_code(IndicatorCodes.lights_on)

    """
        Indicator Bindings
    """

    @Pyro4.expose
    def connect_indicator(self, uri: str) -> None:
        """Connect the Daemon to the Indicator."""

        print_debug("uri:", uri)

        try:
            self.__pyro_indicator = Pyro4.Proxy(uri)
            self.reload_configurations(self.__user)
        except Exception:
            print_warning("Failed initialization")
            print(format_exc())
            self.__pyro_indicator = None

    @Pyro4.expose
    def update_indicator(self) -> None:
        """Update the status (lights on/off) of the indicator."""

        print_debug("state={}".format(self.__lights_state))

        if self.__lights_state:
            self.__indicator_send_code(IndicatorCodes.lights_on)
        else:
            self.__indicator_send_code(IndicatorCodes.lights_off)

    @Pyro4.expose
    def disconnect_indicator(self) -> None:
        """Disconnect the Daemon from the Indicator."""
        self.__pyro_indicator = None

    """
        Private Methods
    """

    def __illuminate_keyboard(self) -> None:

        print_debug()

        # Find the last theme that has been used
        #
        os.utime(self.__theme.path, None)

        # Illuminate the computer lights
        #

        self.__controller.erase_config()

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

        # Update the Indicator
        #
        if self.__pyro_indicator is not None:
            self.__indicator_send_code(IndicatorCodes.lights_on)
            try:
                self.__pyro_indicator.load_profiles(theme_factory._AVAILABLE_THEMES.keys(),
                                                    self.__theme.name,
                                                    self.__lights_state)
            except Exception:
                print_error(format_exc())

        # Update the Daemon variables
        #
        self.__lights_state = True

    def __indicator_send_code(self, code: int) -> None:

        print_debug("code={}".format(code))

        if self.__pyro_indicator is not None:
            try:
                self.__pyro_indicator.set_code(code)
            except Exception:
                print_error(format_exc())


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))  # todo: why is this necessary?

    akbl_daemon = Daemon()
    pyro_daemon = Pyro4.Daemon()
    pyro_uri = str(pyro_daemon.register(akbl_daemon))
    pyro_uri_file = Paths()._daemon_pyro_file
    print_info('Registering URI="{}"\nUpdating "{}"'.format(pyro_uri, pyro_uri_file))
    with open(pyro_uri_file, encoding='utf-8', mode='wt') as f:
        f.write(pyro_uri)

    pyro_daemon.requestLoop()


if __name__ == "__main__":
    main()
