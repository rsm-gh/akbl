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

from copy import copy

# local imports
from utils import print_error, print_debug, hex_to_rgb
from Engine.Request import Request

def parse_area_hex_id(area_hex_id):  
    """
        This method will parse an area_hex_id to a list of three values:

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
        
        AlienFX MSG: gotta check the power button to understand it ..
    """
    parsed_area_hex_id = [0, 0, 0]
    parsed_area_hex_id[0] = area_hex_id // 65536  # pyALienFX: takes the two first digit
    parsed_area_hex_id[1] = area_hex_id // 256 - parsed_area_hex_id[0] * 256  # pyALienFX: takes the four first digit and remove the two first digit
    parsed_area_hex_id[2] = area_hex_id - parsed_area_hex_id[0] * 65536 - parsed_area_hex_id[1] * 256  # pyALienFX: same but remove the first 4 digit

    return parsed_area_hex_id

def adapt_left_color(color):

    if isinstance(color, str):
        color = hex_to_rgb(color)

    r,g,b = color

    adapted_left_color = [0, 0]
    adapted_left_color[0] = int(r * 16 + g)  # pyALienFX: if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
    adapted_left_color[1] = int(b * 16)

    return adapted_left_color

def adapt_right_color(color):
    
    if isinstance(color, str):
        color = hex_to_rgb(color)

    r,g,b = color
    
    adapted_right_color = [0, 0]
    adapted_right_color[0] = int(r)  # pyAlienFX: if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
    adapted_right_color[1] = int(g * 16 + b)

    return adapted_right_color


class Constructor(list):

    def __init__(self, computer, save=False, block=0x01):

        self.computer = computer

        self._block = block        
        self._hex_id = 1
        self._save = save
        self._void = [self.computer.FILL_BYTE] * self.computer.DATA_LENGTH

    def __str__(self):
        return "Constructor: computer.NAME={}, hex_id={}, block={}, _save={}, _void={}".format(self.computer.NAME, self._hex_id, self._block, self._save, self._void)
        
    def save(self, end=False):
        if self._save:
            if not end:
                self.set_save_block(self._block)
            else:
                self.set_save()

    def show_request(self):
        for i in self:
            packet = ''
            for j in i.packet:
                packet += hex(int(j)) + ' '

    def set_speed(self, speed=0xc800):
        self.save()
        legend = "set_speed, speed={}".format(speed)
        
        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_SPEED
        cmd[3] = int(speed / 256)
        cmd[4] = int(speed - (speed / 256) * 256)
        
        self.append(Request(legend, cmd))

    def set_fixed_color(self, area_hex_id, color):
    
        parsed_area_hex_id = parse_area_hex_id(area_hex_id)
        adapted_left_color = adapt_left_color(color)

        self.save()
        legend = "set_fixed_color"
        
        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_COLOR
        cmd[2] = self._hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]
        cmd[7] = adapted_left_color[1]

        self.append(Request(legend, cmd))

    def set_blink_color(self, area_hex_id, color):
        
        parsed_area_hex_id = parse_area_hex_id(area_hex_id)
        adapted_color = adapt_left_color(color)
        
        self.save()
        legend = "set_blink_color, parsed_area_hex_id={}, color={}.".format(color, parsed_area_hex_id)
        
        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_BLINK_COLOR
        cmd[2] = self._hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_color[0]
        cmd[7] = adapted_color[1]

        self.append(Request(legend, cmd))

    def set_color_morph(self, area_hex_id, left_color, right_color):
        
        parsed_area_hex_id = parse_area_hex_id(area_hex_id)
        adapted_left_color = adapt_left_color(left_color)
        adapted_right_color = adapt_right_color(right_color)
        
        self.save()
        color = left_color[1] + right_color[0]
        legend = '''set_color_morph: left_color={}, right_color={}, color={}, parsed_area_hex_id={}.'''.format(left_color, right_color, color, parsed_area_hex_id)

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_MORPH_COLOR
        cmd[2] = self._hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]
        cmd[7] = adapted_left_color[0] + adapted_right_color[1]
        cmd[8] = adapted_right_color[1]

        self.append(Request(legend, cmd))

    def set_save_block(self, block):

        legend = "set_save_block, block={}".format(block)

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE_NEXT
        cmd[2] = block

        self.append(Request(legend, cmd))

    def set_save(self):
        
        legend = "set_save"

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SAVE

        self.append(Request(legend, cmd))

    def get_status(self):

        legend = "get_status"

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_GET_STATUS

        self.append(Request(legend, cmd))

    def reset(self, command=None):
        
        if command is None:
            command = self.computer.RESET_ALL_LIGHTS_ON
            
        if command == self.computer.RESET_ALL_LIGHTS_ON:
            legend = "reset, command=RESET_ALL_LIGHTS_ON"
        elif command == self.computer.RESET_ALL_LIGHTS_OFF:
            legend = "reset, command=RESET_ALL_LIGHTS_OFF"
        elif command == self.computer.RESET_TOUCH_CONTROLS:
            legend = "reset, command=RESET_TOUCH_CONTROLS"
        else:
            legend = "reset, command=UNKNOWN COMMAND !!"
            print_error("Wrong command={}".format(command))
        

        self.save()

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_RESET
        cmd[2] = command

        self.append(Request(legend, cmd))

    def end_line(self):
        self.save()
        legend = "end_line"

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_LOOP_BLOCK_END

        self._hex_id += 0x01
        self.append(Request(legend, cmd))

    def end_config(self):
        self.save(end=True)
        if not self._save:
            legend = "end_config"
            
            cmd = copy(self._void)
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_TRANSMIT_EXECUTE

            self.append(Request(legend, cmd))
