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

class Controller:

    def __init__(self, driver):
        self.driver = driver
        self.constructor = None

    def quit(self):
        sys.exit(0)

    def set_loop(self, action):
        self.wait_for_ok()
        self.driver.write_device(action)

    def set_loop_conf(self, save=False, block=0x01):
        self.constructor = Constructor(self.driver, save, block)
        print('DEBUG Controller: Constructor loaded', self.constructor)

    def add_loop_conf(self, area, mode, left_color, right_color=None):

        if not isinstance(area, list):
            area = self.constructor.parse_areas(area)

        if not isinstance(left_color, list):
            left_color = self.constructor.convert_color(left_color)

        if right_color is not None and not isinstance(right_color, list):
            right_color = self.constructor.convert_color(right_color)

        if mode == 'fixed':
            self.constructor.set_fixed_color(area, left_color)
        elif mode == 'blink':
            self.constructor.set_blink_color(area, left_color)
        elif mode == 'morph' and right_color:
            self.constructor.set_color_morph(area, left_color, right_color)
        else:
            print('Warning: wrong mode `{}` on `add_loop_conf` of `Controller`.'.format(mode))

    def write_conf(self):
        self.wait_for_ok()
        self.driver.write_device(self.constructor)

    def set_color(self, area, color, save=False, Apply=False, block=0x01):

        constructor = Constructor(self.driver, save, block)
        if not isinstance(area, list):
            area = constructor.parse_areas(area)

        if not isinstance(color, list):
            color = constructor.convert_color(color)

        self.wait_for_ok()
        constructor.set_color(area, color)
        constructor.end_loop()
        constructor.end_transfer()
        self.driver.write_device(constructor)

        if Apply:
            self.wait_for_ok()
            constructor = Constructor(self.driver, False, block)
            constructor.set_color(area, color)
            constructor.end_loop()
            constructor.end_transfer()
            self.driver.write_device(constructor)

    def set_color_blink(self, area, color, save=False, Apply=False, block=0x01):
        self.wait_for_ok()
        constructor = Constructor(self.driver, save, block)

        if not isinstance(area, list):
            area = constructor.parse_areas(area)

        if not isinstance(left_color, list):
            left_color = constructor.convert_color(color)

        constructor.set_speed()
        constructor.set_blink_color(area, color)
        constructor.end_loop()
        constructor.end_transfer()
        self.driver.write_device(constructor)

        if Apply:
            self.wait_for_ok()
            constructor = Constructor(self.driver)
            constructor.set_speed()
            constructor.set_blink_color(area, color)
            constructor.end_loop()
            constructor.end_transfer()
            self.driver.write_device(constructor)

    def set_color_morph(self, area, left_color, right_color, save=False, Apply=False, block=0x01):
        self.wait_for_ok()
        constructor = Constructor(self.driver, save, block)

        if not isinstance(Area, list):
            area = constructor.parse_areas(area)

        if not isinstance(left_color, list):
            left_color1 = constructor.convert_color(left_color)

        if not isinstance(right_color, list):
            right_color = constructor.convert_color(right_color)

        constructor.set_speed()
        constructor.set_color_morph(area, left_color1, right_color)
        constructor.end_loop()
        constructor.end_transfer()
        self.driver.write_device(constructor)

        if Apply:
            self.wait_for_ok()
            constructor = Constructor(self.driver, save, block)
            constructor.set_speed()
            constructor.set_color_morph(area, left_color1, right_color)
            constructor.end_loop()
            constructor.end_transfer()
            self.driver.write_device(constructor)

    def wait_for_ok(self):
        self.driver.take_over()
        self.get_state()
        request = Constructor(self.driver)
        request.reset_all()
        self.driver.write_device(request)
        while not self.get_state():
            request.raz()
            request.get_color_status()
            request.reset_all()
            self.driver.write_device(request)
        return True

    def get_state(self):
        self.driver.take_over()
        request = Constructor(self.driver)
        request.get_color_status()
        self.driver.write_device(request)
        msg = self.driver.read_device(request)
        return msg[0] == self.driver.computer.STATE_READY

    def reset(self, res_cmd):
        self.driver.take_over()
        request = Constructor(self.driver)
        while True:
            request.get_color_status()
            self.driver.write_device(request)
            msg = self.driver.read_device(request)
            if msg[0] == 0x10:
                break
            request.raz()
            request.get_color_status()
            request.reset(res_cmd)
            self.driver.write_device(request)
            msg = self.driver.read_device(request)
            if msg[0] == 0x10:
                break
        return True
