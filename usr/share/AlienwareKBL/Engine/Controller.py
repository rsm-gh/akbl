#!/usr/bin/python3
#

#  Copyright (C)  2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
#                 2011-2012  the pyAlienFX team
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

# local imports
from Engine.Constructor import Constructor
from utils import print_debug, print_error, print_warning

class Controller:

    def __init__(self, driver):
        self._driver = driver
        self._constructor = None

    def set_speed(self, speed):
        self._constructor.set_speed(speed)

    def start_config(self, save, block):
        self._constructor = Constructor(self._driver.computer, save, block)
        self._constructor.reset(self._driver.computer.RESET_ALL_LIGHTS_ON)

    def add_line(self, area_hex_id, mode, left_color, right_color=None):

        if mode == 'fixed':
            self._constructor.set_fixed_color(area_hex_id, left_color)
        elif mode == 'blink':
            self._constructor.set_blink_color(area_hex_id, left_color)
        elif mode == 'morph':
            if right_color is None:
                print_warning('trying to set `morph` mode without a `right_color`.The `fixed` mode will be used instead.')
                self._constructor.set_fixed_color(area_hex_id, left_color)
            else:
                self._constructor.set_color_morph(area_hex_id, left_color, right_color)
        else:
            print_warning('wrong mode=`{}`'.format(mode))

        #print('''area=`{}`, mode=`{}`, left_color=`{}`, right_color=`{}`.'''.format(area_hex_id, mode, left_color, right_color))

    def end_line(self):
        self._constructor.end_line()

    def end_config(self):
        self._constructor.end_config()

    def write(self):

        # Wait until is OK to write.
        #
        constructor = Constructor(self._driver.computer)
        constructor.get_status()
        constructor.reset()

        while not self.device_is_ready():
            self._driver.write_constructor(constructor)

        # Write the current constructor
        #
        self._driver.write_constructor(self._constructor)

    def device_is_ready(self):
        self._driver.take_over()
        constructor = Constructor(self._driver.computer)
        constructor.get_status()
        self._driver.write_constructor(constructor)
        msg = self._driver.read_device(constructor)
        return msg[0] == self._driver.computer.STATE_READY

    def reset_all_lights(self, res_cmd):
        self._driver.take_over()
        constructor = Constructor(self._driver.computer)
        constructor.get_status()
        constructor.reset(res_cmd)
        
        while True:
            self._driver.write_constructor(constructor)
            msg = self._driver.read_device(constructor)
            if msg[0] == self._driver.computer.STATE_READY:
                break
                
        return True
