#!/usr/bin/python3
#

#  Copyright (C) 2015-2018  Rafael Senties Martinelli
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
from traceback import format_exc

from AKBL.texts import TEXT_ONLY_ROOT
from AKBL.utils import getuser, print_warning, print_error, string_is_hex_color
from AKBL.Data.Theme import theme_factory
from AKBL.Paths import Paths
from AKBL.CCParser import CCParser
from AKBL.Engine.Controller import Controller

class ConnectDaemon:

    def __init__(self):
        
        self.daemon = Pyro4.Daemon()
        self.paths = Paths()

        uri = self.daemon.register(Daemon(self))
        with open(self.paths._daemon_pyro_file, encoding='utf-8', mode='wt') as f:
            f.write(str(uri))

        self.daemon.requestLoop()


class Daemon:

    def __init__(self, loop_self):
        
        self._controller = Controller()
        
        computer = self._controller.get_computer()
        
        if computer is None:
            exit(1)
            
        self._computer = computer
        
        
        self._COMPUTER_BLOCKS_TO_SAVE = ((True, self._computer.BLOCK_LOAD_ON_BOOT),
                                            #(True, self._computer.BLOCK_STANDBY),
                                            #(True, self._computer.BLOCK_AC_POWER),
                                            #(#True, self._computer.BLOCK_CHARGING),
                                            #(True, self._computer.BLOCK_BATT_SLEEPING),
                                            #(True, self._computer.BLOCK_BAT_POWER),
                                            #(True, self._computer.BLOCK_BATT_CRITICAL),
                                            (False, self._computer.BLOCK_LOAD_ON_BOOT))
        
        self.loop_self = loop_self

        # Initialize the daemon
        #
        self._user = 'root'
        self._paths = Paths()
        self._paths = Paths(self._user)
        self._ccp = CCParser(self._paths.configuration_file, 'GUI Configuration')
        self._indicator_pyro = False
        
        self.reload_configurations(self._user)
        self._lights_state = False
        

    def _iluminate_keyboard(self):

        # Find the last theme that has been used
        #
        os.utime(self._theme.path, None)

        # Iluminate the computer lights
        #
        
        self._controller.erase_config()
        
        for save, block in self._COMPUTER_BLOCKS_TO_SAVE:
                
            self._controller.add_block_line(save=save, block=block)
            self._controller.add_reset_line(self._computer.RESET_ALL_LIGHTS_ON)
            self._controller.add_speed_line(self._theme.get_speed())
            
            for area in self._theme.get_areas():
                for zone in area.get_zones():
                    self._controller.add_color_line(zone.get_hex_id(), zone.get_mode(), zone.get_left_color(), zone.get_right_color())
                
                self._controller.end_colors_line()
                
            self._controller.end_block_line()
            
        self._controller.apply_config()

        # Update the Indicator
        #
        if self._indicator_pyro:
            self._indicator_send_code(100)
            try:
                self._indicator_pyro.load_profiles(theme_factory._AVAILABLE_THEMES.keys(),
                                                   self._theme.name,
                                                   self._lights_state)
            except Exception:
                print_error(format_exc())

        # Update the Daemon variables
        #
        self._lights_state = True

    def _indicator_send_code(self, val):
        if self._indicator_pyro:
            try:
                self._indicator_pyro.set_code(val)
            except Exception:
                print_error(format_exc())

    """
        General Bindings
    """
    @Pyro4.expose
    def ping(self):
        pass

    @Pyro4.expose
    def reload_configurations(self, user, indicator=True, set_default=True):

        if user != self._user:
            self._user = user
            self._paths = Paths(user)
            self._ccp.set_configuration_path(self._paths.configuration_file)

        theme_factory.LOAD_profiles(self._computer, self._paths._profiles_dir)

        if set_default:
            _, profile_name = theme_factory.GET_last_configuration()
            self._theme = theme_factory.get_theme_by_name(profile_name)

        if self._indicator_pyro and indicator:
            try:
                self._indicator_pyro.load_profiles(theme_factory._AVAILABLE_THEMES.keys(), 
                                                   self._theme.name, 
                                                   self._lights_state)
            except Exception:
                print_error(format_exc())

    """
        Bindings for the users
    """
    @Pyro4.expose
    def set_profile(self, user, profile):
        """
            Set a profile from the existing profiles.

            + 'profile' is the profile name
        """
        if user != self._user:
            self._user = user
            self._paths = Paths(user)

        self.reload_configurations(user, False, False)

        if profile in theme_factory._AVAILABLE_THEMES.keys():
            self._theme = theme_factory._AVAILABLE_THEMES[profile]
            self._iluminate_keyboard()

    @Pyro4.expose
    def switch_lights(self, user):
        """
            If the lights are on, put them off
            or if the lights are off put them on
        """
        if self._lights_state:
            self.set_lights(user, False)
        else:
            self.set_lights(user, True)

    @Pyro4.expose
    def set_lights(self, user_name, state):
        """
            Turn the lights on or off, 'state' can be a boolean or a string.
        """
        if user_name != self._user:
            self.reload_configurations(user_name)
        
        if state in (False, 'False', 'false'):

            areas_to_keep_on = self._ccp.get_str_defval('areas_to_keep_on', '')

            print_warning("AREAS TO KEEP ON")
            print_warning(areas_to_keep_on)


            if areas_to_keep_on == '':
                
                self._controller.erase_config()
                
                for save, block in self._COMPUTER_BLOCKS_TO_SAVE:
                    self._controller.add_block_line(save, block)
                    self._controller.add_reset_line(self._computer.RESET_ALL_LIGHTS_OFF)
                    
                self._controller.apply_config()
            else:
                """
                    To turn off the lights but let some areas on, instead of sending the command "all the lights off",
                    some areas are set to black color.
                """
                
                
                areas_to_keep_on = areas_to_keep_on.split('|')

                print_warning(areas_to_keep_on)

                self._controller.erase_config()
                for save, block in self._COMPUTER_BLOCKS_TO_SAVE:
                    
                    self._controller.add_block_line(save, block)
                    self._controller.add_reset_line(self._computer.RESET_ALL_LIGHTS_ON)
                    self._controller.add_speed_line(1)

                    for area in self._theme.get_areas():
                        if not area.name in areas_to_keep_on:
                            for zone in area.get_zones():
                                self._controller.add_color_line(zone.get_hex_id(), 'fixed', '#000000', '#000000')
                            self._controller.end_colors_line()
                    self._controller.end_block_line()
                self._controller.apply_config()

            self._lights_state = False
            self._indicator_send_code(150)
        else:
            self._iluminate_keyboard()

    @Pyro4.expose
    def set_colors(self, mode, speed, left_colors, right_colors=None):
        """
            Change the colors and the mode of the keyboard.

            + The available modes are: 'fixed', 'morph', 'blink'
                'fixed' and 'blink' only takes left_colors

            + Speed must be an integer. 1 =< speed =< 256

            + left_colors and right_colors can be a single hex color or a list of hex_colors.
              If both arguments are used, they must have the same number of items.
        """

        if mode not in ('fixed', 'morph', 'blink'):
            print_warning("Wrong mode" + str(mode))
            return
        elif not isinstance(speed, int):
            print_warning("The speed argument must be an integer.")
            return
        elif speed > 255:
            print_warning("The speed argument exeeds the limit > 255.")
            return
        elif speed < 1:
            print_warning("The speed argument must be >= 1.")
            return

        if not isinstance(left_colors, list) and not isinstance(left_colors, tuple):
            left_colors = [left_colors]

        if right_colors is None:
            right_colors = left_colors
            
        elif not isinstance(right_colors, list) and not isinstance(right_colors, tuple):
            right_colors = [right_colors]

        if len(left_colors) != len(right_colors):
            print_warning("The colors lists must have the same lenght.")
            return
            
        for color_list in (left_colors, right_colors):
            for color in color_list:
                if not string_is_hex_color(color):
                    print_warning("The colors argument must only contain hex colors. The color={} is not valid.".format(color))
                    return
                    
        
        self._controller.erase_config()

        for save, block in self._COMPUTER_BLOCKS_TO_SAVE:

            self._controller.add_block_line(save, block)
            self._controller.add_reset_line(self._computer.RESET_ALL_LIGHTS_ON)
            self._controller.add_speed_line(speed)

            for region in self._computer.get_regions():
                for i, (left_color, right_color) in enumerate(zip(left_colors, right_colors)):
                    
                    if i + 1 > region.max_commands:
                        print_warning("The number of maximum commands for the region={} have been exeed. The loop was stopped at {}.".format(region.name, i+1))
                        break
                    
                    if mode == 'blink':
                        if region.can_blink:
                            self._controller.add_color_line(region.hex_id, 'blink', left_color, right_color)
                        else:
                            self._controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning("The mode=blink is not supported for the region={}, the mode=fixed will be used instead.".format(region.name))
                            
                    elif mode == 'morph':
                        if region.can_morph:
                            self._controller.add_color_line(region.hex_id, 'morph', left_color, right_color)
                        else:
                            self._controller.add_color_line(region.hex_id, 'fixed', left_color)
                            print_warning("The mode=morph is not supported for the region={}, the mode=fixed will be used instead.".format(region.name))
                            
                    else:
                        self._controller.add_color_line(region.hex_id, 'fixed', left_color)
                    
                self._controller.end_colors_line()

            self._controller.end_block_line()
        
        self._controller.apply_config()
        
        self._lights_state = True

    """
        Bindings for the graphical interphase
    """
    
    @Pyro4.expose
    def get_computer_name(self):
        return self._computer.NAME

    @Pyro4.expose
    def get_computer_info(self):
        return (self._computer.NAME, self._computer.VENDOR_ID, self._computer.PRODUCT_ID, self._controller.get_device_information())

    @Pyro4.expose
    def modify_lights_state(self, value):
        """
            This method does not changes the lights of the keyboard,
            it only updates the daemon and the indicator
        """
        if value in (False, 'False', 'false'):
            self._lights_state = False
            self._indicator_send_code(150)
        else:
            self._lights_stae = True
            self._indicator_send_code(100)

    """
        Indicator Bindings
    """

    @Pyro4.expose
    def indicator_get_state(self):
        if self._lights_state:
            self._indicator_send_code(100)
        else:
            self._indicator_send_code(150)

    @Pyro4.expose
    def indicator_init(self, uri):
        try:
            self._indicator_pyro = Pyro4.Proxy(str(uri))
            self.reload_configurations(self._user)
        except Exception:
            print_warning("Failed initialization")
            print(format_exc())
            self._indicator_pyro = False

    @Pyro4.expose
    def indicator_kill(self):
        self._indicator_pyro = False


def main():
    if getuser() != 'root':
        print(TEXT_ONLY_ROOT)
    else:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        _=ConnectDaemon()
