#!/usr/bin/python3
#

#  Copyright (C)  2014-2016  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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

from Engine.Constructor import Constructor
from utils import print_debug, print_error, hex_to_rgb

class Controller:

    def __init__(self, driver):
        self._driver = driver
        self._constructor = None

    def add_loop(self, area_hex_id, mode, left_color, right_color=None):

        if not isinstance(area_hex_id, list):
            parsed_area_hex_id = self._constructor.parse_areas(area_hex_id)
        else:
            parsed_area_hex_id = area_hex_id

        if not isinstance(left_color, list):
            left_color = hex_to_rgb(left_color)

        if right_color is not None and not isinstance(right_color, list):
            right_color = hex_to_rgb(right_color)

        if mode == 'fixed':
            self._constructor.set_fixed_color(parsed_area_hex_id, left_color)
        elif mode == 'blink':
            self._constructor.set_blink_color(parsed_area_hex_id, left_color)
        elif mode == 'morph' and right_color:
            self._constructor.set_color_morph(parsed_area_hex_id, left_color, right_color)
        else:
            print_error('wrong mode=`{}`'.format(mode))

        #print_debug('''area=`{}`, mode=`{}`, left_color=`{}`, right_color=`{}`.'''.format(area_hex_id, mode, left_color, right_color))


    def set_speed(self, speed):
        self._constructor.set_speed(speed)
            
    def end_transfer(self):
        self._constructor.end_transfer()

    def end_loop(self):
        self._constructor.end_loop()

    def start_loop(self, save, block):
        self._constructor = Constructor(self._driver.computer, save, block)
        print_debug(self._constructor)

    def write(self):
        # Wait until is OK to write.
        #
        print_debug('Waiting for OK..')
        self._driver.take_over()
        self.get_state()
        constructor = Constructor(self._driver.computer)
        constructor.reset_all()
        self._driver.write_device(constructor)
        while not self.get_state():
            constructor.raz()
            constructor.get_color_status()
            constructor.reset_all()
            self._driver.write_device(constructor)
        # Write
        #
        print_debug('Writing the constructor..')
        self._driver.write_device(self._constructor)

    def get_state(self):
        self._driver.take_over()
        constructor = Constructor(self._driver.computer)
        constructor.get_color_status()
        self._driver.write_device(constructor)
        msg = self._driver.read_device(constructor)
        return msg[0] == self._driver.computer.STATE_READY

    def reset(self, res_cmd):
        self._driver.take_over()
        constructor = Constructor(self._driver.computer)
        while True:
            constructor.get_color_status()
            self._driver.write_device(constructor)
            msg = self._driver.read_device(constructor)
            if msg[0] == 0x10:
                break
            constructor.raz()
            constructor.get_color_status()
            constructor.reset(res_cmd)
            self._driver.write_device(constructor)
            msg = self._driver.read_device(constructor)
            if msg[0] == 0x10:
                break
        return True
