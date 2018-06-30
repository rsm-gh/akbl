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

import sys
from copy import copy

from AKBL.utils import print_error, print_debug, print_warning, rgb_to_hex
from AKBL.Engine.Core.Request import Request

class Constructor(list):

    def __init__(self, computer, save=False, block=1):

        self.computer = computer

        self._block = block
        self._hex_id = 1
        self._save = save
        self._void = [self.computer.FILL_BYTE] * self.computer.DATA_LENGTH

    def __str__(self):
        return "Constructor: computer.NAME={}, hex_id={}, block={}, _save={}, _void={}".format(self.computer.NAME, self._hex_id, self._block, self._save, self._void)
        
    def _adapt_area_hex_id(self, area_hex_id):  
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

    def _adapt_left_color(self, color):

        if isinstance(color, list):
            color = rgb_to_hex(color)
            
        color = color.replace("#",'')

        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16
        c = [0x00, 0x00]
        c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = b * 16
        return c

    def _adapt_right_color(self, color):

        if isinstance(color, list):
            color = rgb_to_hex(color)
            
        color = color.replace("#",'')

        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16
        c = [0x00, 0x00]
        c[0] = r  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = g * 16 + b
        return c

    def _save_line(self):
        if self._save:
            
            legend = "_save_block, block={}".format(self._block)
            
            cmd = copy(self._void)
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_SAVE_NEXT
            cmd[2] = self._block

            self.append(Request(legend, cmd))

    def _save_block(self):
        if self._save:
            
            legend = "_save_block"
            
            cmd = copy(self._void)
            cmd[0] = self.computer.START_BYTE
            cmd[1] = self.computer.COMMAND_SAVE
            
            self.append(Request(legend, cmd))   
        
    def raz(self):
        self.clear()
        self._hex_id = 1
        
    def show_request(self):
        for i in self:
            packet = ''
            for j in i.packet:
                packet += hex(int(j)) + ' '

    def set_block(self, save, block):
        self._save = save
        self._block = block
        self._hex_id = 1
        

    def set_speed(self, speed):
        
        speed=int(speed)
        
        if speed > 255:
            speed = 255
            print_warning("the speed can not be > 255, it will be set equal to 255.")
        elif speed <= 0:
            speed = 1
            print_warning("The speed can not be =< 0, it will be set equal to 1.")
        
        
        self._save_line()
        
        legend = "set_speed, speed={}\n".format(speed)
        
        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_SPEED
        cmd[3] = int(speed)
        
        self.append(Request(legend, cmd))

    def set_fixed_color(self, area_hex_id, color):
    
        self._save_line()
        
        legend = '''set_fixed_color: left_color={}, hex_id={}'''.format(color, area_hex_id)
        
        parsed_area_hex_id = self._adapt_area_hex_id(area_hex_id)
        adapted_left_color = self._adapt_left_color(color)

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
                
        self._save_line()
        
        legend = "set_blink_color:color={}, hex_id={}".format(color, area_hex_id)
        
        parsed_area_hex_id = self._adapt_area_hex_id(area_hex_id)
        adapted_color = self._adapt_left_color(color)
        
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
                
        self._save_line()
        
        legend = '''set_morph_color: left_color={}, right_color={}, hex_id={}'''.format(left_color, right_color, area_hex_id)

        parsed_area_hex_id = self._adapt_area_hex_id(area_hex_id)
        adapted_left_color = self._adapt_left_color(left_color)
        adapted_right_color = self._adapt_right_color(right_color)

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_SET_MORPH_COLOR
        cmd[2] = self._hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]
        cmd[7] = adapted_left_color[1] + adapted_right_color[0]
        cmd[8] = adapted_right_color[1]

        self.append(Request(legend, cmd))

    def set_get_status(self):

        legend = "set_get_status"

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_GET_STATUS

        self.append(Request(legend, cmd))

    def set_reset_line(self, command=None):
        
        if command is None:
            command = self.computer.RESET_ALL_LIGHTS_ON
            
        if command == self.computer.RESET_ALL_LIGHTS_ON:
            legend = "reset, command=RESET_ALL_LIGHTS_ON\n"
            
        elif command == self.computer.RESET_ALL_LIGHTS_OFF:
            legend = "reset, command=RESET_ALL_LIGHTS_OFF\n"
            
        elif command == self.computer.RESET_TOUCH_CONTROLS:
            legend = "reset, command=RESET_TOUCH_CONTROLS\n"
            
        else:
            legend = "reset, command=UNKNOWN COMMAND !!\n"
            print_error("Wrong command={}".format(command))
        
        self._save_line()

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_RESET
        cmd[2] = command

        self.append(Request(legend, cmd))

    def set_end_colors_line(self):
        
        self._save_line()
        
        legend = "end_colors_line\n"

        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_LOOP_BLOCK_END

        self._hex_id += 1
        self.append(Request(legend, cmd))

    def set_end_block_line(self):
        
        self._save_block()
        
        legend = "end_block_line\n\n"
        
        cmd = copy(self._void)
        cmd[0] = self.computer.START_BYTE
        cmd[1] = self.computer.COMMAND_TRANSMIT_EXECUTE

        self.append(Request(legend, cmd))

