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


import sys
import os
import time
import usb
from copy import copy
from traceback import format_exc

# local imports
from Computers import AllComputers, CommonConf


class Driver(AllComputers):

    def __init__(self):
        # Define I/O Reqquest types
        self.SEND_REQUEST_TYPE = 0x21
        self.SEND_REQUEST = 0x09
        self.SEND_VALUE = 0x202
        self.SEND_INDEX = 0x00
        self.READ_REQUEST_TYPE = 0xa1
        self.READ_REQUEST = 0x01
        self.READ_VALUE = 0x101
        self.READ_INDEX = 0x0

        self.computer = None
        self._device = None
        self._device_found = False

    def has_device(self):
        if self._device is None:
            return False
        return True

    def find_device(self, id_vendor=False, id_product=False):
        """
            Look for all the devices listed in the `Computer.py` file.
            If a computer is finded, the device is loaded as well as 
            all the parameters of the computer.
        """

        if id_vendor and id_product:
            try:
                device = usb.core.find(idVendor=id_vendor, idProduct=id_product)
            except Exception as e:
                print(format_exc())

                if device is not None:
                    self.computer_name = 'Block Testing'
                    self.vendor_id = id_vendor
                    self.product_id = id_product
                    self.computer = CommonConf()
                    self._device = device
                    self.take_over()
                    return

        for computer_name in sorted(self.computers_list.keys()):
            device = usb.core.find(
                idVendor=self.computers_list[computer_name].vendor_id,
                idProduct=self.computers_list[computer_name].product_id)

            if device is not None:

                # This hack was made to differenciate the M14XR1 from the M14XR2R2
                if computer == 'M14XR1' and 'Gaming' in str(dev):
                    computer = 'M14XR2'

                self.computer_name = computer
                self.computer = self.computers_list[computer_name].computer
                self.vendor_id = self.computers_list[computer_name].vendor_id
                self.product_id = self.computers_list[computer_name].product_id
                self._device = device
                self.take_over()
                return

    def write_device(self, MSG):
        if len(MSG[0].packet) == self.computer.DATA_LENGTH:
            for msg in MSG:
                time.sleep(0.02)
                self._device.ctrl_transfer(
                    self.SEND_REQUEST_TYPE,
                    self.SEND_REQUEST,
                    self.SEND_VALUE,
                    self.SEND_INDEX,
                    msg.packet)
        else:
            self._device.ctrl_transfer(
                self.SEND_REQUEST_TYPE,
                self.SEND_REQUEST,
                self.SEND_VALUE,
                self.SEND_INDEX,
                MSG)

    def read_device(self, msg):
        msg = self._device.ctrl_transfer(
            self.READ_REQUEST_TYPE, 
            self.READ_REQUEST, 
            self.READ_VALUE, 
            self.READ_INDEX, 
            len(msg[0].packet))

        return msg

    def take_over(self):
        try:
            self._device.set_configuration()
        except:
            self._device.detach_kernel_driver(0)
            try:
                self._device.set_configuration()
            except Exception as e:
                raise DeviceNotFound("Can't set the configuration. Error: {}".format(e))
                sys.exit(1)


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

    def add_speed_conf(self, speed=0xc800):
        self.constructor.set_speed(speed)

    def end_loop_conf(self):
        self.constructor.end_loop()

    def end_transfer_conf(self):
        self.constructor.end_transfer()

    def write_conf(self):
        self.wait_for_ok()
        self.driver.write_device(self.request)

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


class Constructor(list):

    def __init__(self, driver, save=False, block=0x01):
        self.raz()
        self.computer = driver.computer
        self.void = [self.computer.FILL_BYTE] * self.computer.DATA_LENGTH
        self.Id = 0x01
        self.save = save
        self.block = block

    def save(self, end=False):
        if self.save:
            if not end:
                self.set_save_block(self.block)
            else:
                self.set_save()

    def show_request(self):
        for i in self:
            packet = ''
            for j in i.packet:
                packet += hex(int(j)) + ' '

    def set_speed(self, speed=0xc800):
        self.save()
        cmd = copy(self.void)
        legend = "set_speed =  {}".format(speed)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_SPEED
        cmd[3] = int(Speed / 256)
        cmd[4] = int(Speed - (Speed / 256) * 256)
        self.append(Request(legend, cmd))

    def set_blink_color(self, area, color):
        self.save()
        cmd = copy(self.void)
        legend = "set_blink_color `{}` on area `{}`".format(color, area)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_BLINK_COLOR
        cmd[2] = self.Id
        cmd[3] = area[0]
        cmd[4] = area[1]
        cmd[5] = area[2]
        cmd[6] = left_color[0]
        cmd[7] = left_color[1]
        self.append(Request(legend, cmd))

    def set_color_morph(self, area, left_color, right_color):
        self.save()
        cmd = copy(self.void)
        color = left_color[1] + right_color[0]
        legend = '''set_color_morph:
            left_color: `{}`
            right_color: `{}`
            color: `{}`
            area: `{}`
            '''.format(left_color, right_color, color, area)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_MORPH_COLOR
        cmd[2] = self.Id
        cmd[3] = area[0]
        cmd[4] = area[1]
        cmd[5] = area[2]
        cmd[6] = left_color[0]
        cmd[7] = color
        cmd[8] = right_color[1]

        self.append(Request(legend, cmd))

    def parse_areas(self, areas):  # gotta check the power button to understand it ...
        """
            This method will parse an area to a list of three values.

            area = 0x000000

            0x80    -> [0x0, 0x0, 0x80]
            0x100   -> [0x0, 0x1, 0x0]
            0x2     -> [0x0, 0x0, 0x2]
            0x1     -> [0x0, 0x0, 0x1]
            0x20    -> [0x0, 0x0, 0x20]
            0x1c00  -> [0x0, 0x1c, 0x0]
            0x4     -> [0x0, 0x0, 0x4]
            0x8     -> [0x0, 0x0, 0x8]
            0x40    -> [0x0, 0x0, 0x40]
            0x200   -> [0x0, 0x2, 0x0]
        """

        ret = [0x00, 0x00, 0x00]

        if isinstance(areas, dict):
            for key in areas:
                print(key)
                area += self.computer.regions[key].regionId

        elif isinstance(areas, int):
            area = areas

        elif isinstance(areas, str):
            area = int(areas, 16)

        # Takes the two first digit
        ret[0] = area // 65536
        # Takes the four first digit and remove the two first digit
        ret[1] = area // 256 - ret[0] * 256
        ret[2] = area - ret[0] * 65536 - ret[1] * 256  # Same but remove the first 4 digit

        return ret

    def set_color(self, Area, left_color, hex_id=0x01):

        self.save()
        cmd = copy(self.void)
        legend = "Set left_color"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_COLOR
        cmd[2] = self.hex_id
        cmd[3] = Area[0]
        cmd[4] = Area[1]
        cmd[5] = Area[2]
        cmd[6] = left_color[0]
        cmd[7] = left_color[1]

        self.append(Request(legend, cmd))

    def set_save_block(self, block):
        cmd = copy(self.void)
        legend = "save block: {}".format(block)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE_NEXT
        cmd[2] = block

        self.append(Request(legend, cmd))

    def set_save(self):
        cmd = copy(self.void)
        legend = "Set save"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE

        self.append(Request(legend, cmd))

    def convert_color(self, color):
        color = color.replace('#', '')
        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16
        c = [0x00, 0x00]
        c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = b * 16
        return c

    def get_color_status(self):
        cmd = copy(self.void)
        legend = "get_color_status"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_GET_STATUS

        self.append(Request(legend, cmd))

    def reset_all(self):
        self.save()
        cmd = copy(self.void)
        legend = "reset_all"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_RESET
        cmd[2] = self.computer.RESET_ALL_LIGHTS_ON

        self.append(Request(legend, cmd))

    def reset(self, command):
        if command in [self.computer.RESET_ALL_LIGHTS_ON,
                       self.computer.RESET_ALL_LIGHTS_OFF,
                       self.computer.RESET_TOUCH_CONTROLS,
                       self.computer.RESET_SLEEP_LIGHTS_ON]:

            self.save()
            cmd = copy(self.void)
            legend = "reset"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_RESET
            cmd[2] = command

            self.append(Request(legend, cmd))
        else:
            print("Engine > Constructor error: WRONG RESET COMMAND")

    def end_loop(self):
        self.save()
        cmd = copy(self.void)
        legend = "end_loop"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_LOOP_BLOCK_END

        self.Id += 0x01
        self.append(Request(legend, cmd))

    def end_transfer(self):
        self.save(end=True)
        if not self.save:
            cmd = copy(self.void)
            legend = "end_transfert"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_TRANSMIT_EXECUTE

            self.append(Request(legend, cmd))

    def raz(self):
        while len(self) > 0:
            self.pop()


class Request:

    def __init__(self, legend, packet):
        self.legend = legend
        self.packet = packet
