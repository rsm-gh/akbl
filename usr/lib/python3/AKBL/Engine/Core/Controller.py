#!/usr/bin/python3
#

#  Copyright (C)  2014-2018  Rafael Senties Martinelli 
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


from AKBL.utils import print_error, print_warning
from AKBL.Engine.Core.Driver import Driver
from AKBL.Engine.Core.Constructor import Constructor

class Controller:

    def __init__(self, driver=Driver()):
            
        if not driver.has_device():
            print_error("The computer is not supported.")
            self._driver = None
        else:
            self._driver = driver
            self._constructor = Constructor(self._driver.computer)

    def _device_is_ready(self):
        
        self._driver.take_over()
        
        constructor = Constructor(self._driver.computer)
        constructor.set_get_status()
        
        self._driver.write_constructor(constructor)
        msg = self._driver.read_device(constructor)
        return msg[0] == self._driver.computer.STATE_READY

    def get_computer(self):
        if not self._driver is None and self._driver.has_device():
            return self._driver.computer
    
        return None

    def get_device_information(self):
        if self._driver.has_device():
            return str(self._driver._device)
            
        return None

    def erase_config(self):
        self._constructor.raz()

    def add_block_line(self, save, block):
        self._constructor.set_block(save, block)

    def add_reset_line(self, res_cmd):
        
        self._driver.take_over()
        
        constructor = Constructor(self._driver.computer)
        constructor.set_get_status()
        constructor.set_reset_line(res_cmd)
        
        while not self._device_is_ready():
            self._driver.write_constructor(constructor)
                
        return True

    def add_speed_line(self, speed):
        self._constructor.set_speed(speed)

    def add_color_line(self, area_hex_id, mode, left_color, right_color=None):

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

    def end_colors_line(self):
        self._constructor.set_end_colors_line()

    def end_block_line(self):
        self._constructor.set_end_block_line()

    def apply_config(self):

        # Wait until is OK to write.
        #
        constructor = Constructor(self._driver.computer)
        constructor.set_get_status()
        constructor.set_reset_line()

        while not self._device_is_ready():
            self._driver.write_constructor(constructor)

        # Write the current constructor
        #
        self._driver.write_constructor(self._constructor)
