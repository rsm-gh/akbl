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

from copy import copy

class Request:

    def __init__(self, legend, packet):
        self.legend = legend
        self.packet = packet


class Constructor(list):

    def __init__(self, driver, save=False, block=0x01):
        self.raz()
        self.computer = driver.computer
        self.Id = 0x01
        self.block = block
        
        self._save = save
        self._void = [self.computer.FILL_BYTE] * self.computer.DATA_LENGTH

    def save(self, end=False):
        if self:
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
        cmd = copy(self._void)
        legend = "set_speed =  {}".format(speed)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_SPEED
        cmd[3] = int(speed / 256)
        cmd[4] = int(speed - (speed / 256) * 256)
        self.append(Request(legend, cmd))

    def set_blink_color(self, area, color):
        self.save()
        cmd = copy(self._void)
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
        cmd = copy(self._void)
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

    def parse_areas(self, areas):  # gotta check the power button to understand it ..
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
        cmd = copy(self._void)
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
        cmd = copy(self._void)
        legend = "save block: {}".format(block)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE_NEXT
        cmd[2] = block

        self.append(Request(legend, cmd))

    def set_save(self):
        cmd = copy(self._void)
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
        cmd = copy(self._void)
        legend = "get_color_status"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_GET_STATUS

        self.append(Request(legend, cmd))

    def reset_all(self):
        self.save()
        cmd = copy(self._void)
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
            cmd = copy(self._void)
            legend = "reset"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_RESET
            cmd[2] = command

            self.append(Request(legend, cmd))
        else:
            print("Engine > Constructor error: WRONG RESET COMMAND")

    def end_loop(self):
        self.save()
        cmd = copy(self._void)
        legend = "end_loop"
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_LOOP_BLOCK_END

        self.Id += 0x01
        self.append(Request(legend, cmd))

    def end_transfer(self):
        self.save(end=True)
        if not self._save:
            cmd = copy(self._void)
            legend = "end_transfert"
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_TRANSMIT_EXECUTE

            self.append(Request(legend, cmd))

    def raz(self):
        for request in self:
            self.pop(request)
