#!/usr/bin/python3
#

#  Copyright (C) 2014-2019, 2024 Rafael Senties Martinelli.
#                2011-2012 the pyAlienFX team.
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

from AKBL.Engine.Driver import Driver
from AKBL.Engine.Constructor import Constructor
from AKBL.utils import print_warning, print_error, print_debug

class Controller:

    def __init__(self, computer):

        self.__driver = None
        self.__computer = None
        self.__constructor = None

        self.set_computer(computer)

    def set_computer(self, computer):
        self.__computer = computer

        driver = Driver()
        driver.load_device(self.__computer.vendor_id,
                           self.__computer.product_id)

        if driver.has_device():
            self.__driver = driver
            self.__constructor = Constructor(computer)
            print_debug("Driver loaded with computer", self.__computer.name)
            return True

        self.__driver = None
        self.__constructor = None
        print_error("The computer '{}' is not supported by this hardware.".format(self.__computer.name))
        return False

    def get_computer(self):
        return self.__computer

    def get_device_information(self):
        if self.__driver is not None:
            return self.__driver.device_information()

    def erase_config(self):
        if self.__constructor is not None:
            self.__constructor.clear()

    def add_block_line(self, save, block):
        if self.__constructor is not None:
            self.__constructor.set_block(save, block)

    def add_reset_line(self, res_cmd):

        if self.__driver is None or self.__computer is None:
            return

        self.__driver.take_over()
        
        constructor = Constructor(self.__computer)
        constructor.set_get_status()
        constructor.set_reset_area(res_cmd)
        
        while not self.__device_is_ready():
            self.__driver.write_constructor(constructor)
                
        return True

    def add_speed_line(self, speed):
        if self.__constructor is not None:
            self.__constructor.set_speed(speed)

    def add_color_line(self, area_hex_id, mode, left_color, right_color=None):

        if self.__constructor is None:
            return

        elif mode == 'fixed':
            self.__constructor.add_light_zone(area_hex_id, left_color)

        elif mode == 'blink':
            self.__constructor.add_blink_zone(area_hex_id, left_color)

        elif mode == 'morph':
            if right_color is None:
                print_warning('trying to set `morph` mode without a `right_color`.The `fixed` mode will be used instead.')
                self.__constructor.add_light_zone(area_hex_id, left_color)
            else:
                self.__constructor.add_morph_zone(area_hex_id, left_color, right_color)
        else:
            print_warning('wrong mode=`{}`'.format(mode))

    def end_colors_line(self):
        if self.__constructor is not None:
            self.__constructor.set_end_colors_line()

    def end_block_line(self):
        if self.__constructor is not None:
            self.__constructor.set_end_block_line()

    def apply_config(self):

        if self.__driver is None or self.__computer is None:
            return

        # Wait until is OK to write.
        #
        constructor = Constructor(self.__computer)
        constructor.set_get_status()
        constructor.set_reset_area()

        while not self.__device_is_ready():
            self.__driver.write_constructor(constructor)

        # Write the current constructor
        #
        self.__driver.write_constructor(self.__constructor)
        
    def __device_is_ready(self):

        if self.__driver is None or self.__computer is None:
            print_error("Calling device ready with no driver and computer.")
            return True # To stop the loops.
        
        self.__driver.take_over()
        
        constructor = Constructor(self.__computer)
        constructor.set_get_status()
        
        self.__driver.write_constructor(constructor)
        msg = self.__driver.read_device(constructor)
        return msg[0] == self.__computer.state_ready
