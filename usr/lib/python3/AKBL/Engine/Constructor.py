#!/usr/bin/python3
#

#  Copyright (C) 2014-2018 Rafael Senties Martinelli.
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

from AKBL.Engine.Command import Command
from AKBL.utils import rgb_to_hex
from AKBL.console import print_error, print_warning


class Constructor:

    def __init__(self, computer, save=False, block=1):

        self.__computer = computer
        self.__commands = []
        self.__block = block
        self.__hex_id = 1
        self.__save = save

    def __str__(self):
        return "Constructor: computer.name={}, hex_id={}, block={}, _save={}".format(self.__computer.name,
                                                                                     self.__hex_id,
                                                                                     self.__block,
                                                                                     self.__save)

    def __iter__(self):
        for command in self.__commands:
            yield command

    def get_first_command(self):

        if len(self.__commands) > 0:
            return self.__commands[0]

        return None

    def set_block(self, save, block):
        self.__save = save
        self.__block = block
        self.__hex_id = 1

    def set_speed(self, speed):

        speed = int(speed)

        if speed > 255:
            speed = 255
            print_warning("the speed can not be > 255, it will be set equal to 255.")
        elif speed < 0:
            speed = 0
            print_warning("The speed can not be < 0, it will be set equal to 0.")

        self.__save_line()

        legend = "set_speed, speed={}\n".format(speed)

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_set_speed
        cmd[3] = int(speed)

        self.__commands.append(Command(legend, cmd))

    def add_light_zone(self, area_hex_id, color):

        self.__save_line()

        legend = '''add_light_zone: left_color={}, hex_id={}'''.format(color, area_hex_id)

        parsed_area_hex_id = self.__adapt_area_hex_id(area_hex_id)
        adapted_left_color = self.__adapt_left_color(color)

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_set_color
        cmd[2] = self.__hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]
        cmd[7] = adapted_left_color[1]

        self.__commands.append(Command(legend, cmd))

    def add_blink_zone(self, area_hex_id, color):

        self.__save_line()

        legend = "add_blink_zone:color={}, hex_id={}".format(color, area_hex_id)

        parsed_area_hex_id = self.__adapt_area_hex_id(area_hex_id)
        adapted_color = self.__adapt_left_color(color)

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_set_blink_color
        cmd[2] = self.__hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_color[0]
        cmd[7] = adapted_color[1]

        self.__commands.append(Command(legend, cmd))

    def add_morph_zone(self, area_hex_id, left_color, right_color):

        self.__save_line()

        legend = '''add_morph_zone: left_color={}, right_color={}, hex_id={}'''.format(left_color,
                                                                                       right_color,
                                                                                       area_hex_id)

        parsed_area_hex_id = self.__adapt_area_hex_id(area_hex_id)
        adapted_left_color = self.__adapt_left_color(left_color)
        adapted_right_color = self.__adapt_right_color(right_color)

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_set_morph_color
        cmd[2] = self.__hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]
        cmd[7] = adapted_left_color[1] + adapted_right_color[0]
        cmd[8] = adapted_right_color[1]

        self.__commands.append(Command(legend, cmd))

    def set_get_status(self):

        legend = "set_get_status"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_get_status

        self.__commands.append(Command(legend, cmd))

    def set_reset_area(self, command=None):

        if command is None:
            command = self.__computer.reset_all_lights_on

        if command == self.__computer.reset_all_lights_on:
            legend = "reset, command=RESET_ALL_LIGHTS_ON\n"

        elif command == self.__computer.reset_all_lights_off:
            legend = "reset, command=RESET_ALL_LIGHTS_OFF\n"

        elif command == self.__computer.reset_touch_controls:
            legend = "reset, command=RESET_TOUCH_CONTROLS\n"

        else:
            legend = "reset, command=UNKNOWN COMMAND !!\n"
            print_error("Wrong command={}".format(command))

        self.__save_line()

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_reset
        cmd[2] = command

        self.__commands.append(Command(legend, cmd))

    def set_end_colors_line(self):

        self.__save_line()

        legend = "end_colors_line\n"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_loop_block_end

        self.__hex_id += 1
        self.__commands.append(Command(legend, cmd))

    def set_end_block_line(self):

        self.__save_block()

        legend = "end_block_line\n\n"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_transmit_execute

        self.__commands.append(Command(legend, cmd))

    def clear(self):
        self.__commands.clear()
        self.__hex_id = 1

    @staticmethod
    def __adapt_area_hex_id(area_hex_id):
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
            
            AlienFX MSG: gotta check the power button to understand it ...
        """
        parsed_area_hex_id = [0, 0, 0]

        # pyALienFX: takes the two first digits
        parsed_area_hex_id[0] = area_hex_id // 65536

        # pyALienFX: takes the four first digits and remove the two first digits
        parsed_area_hex_id[1] = area_hex_id // 256 - parsed_area_hex_id[0] * 256

        # pyALienFX: same but remove the first 4 digits
        parsed_area_hex_id[2] = area_hex_id - parsed_area_hex_id[0] * 65536 - parsed_area_hex_id[1] * 256

        return parsed_area_hex_id

    @staticmethod
    def __adapt_left_color(color):

        if isinstance(color, list):
            color = rgb_to_hex(color)

        color = color.replace("#", '')

        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16
        c = [0x00, 0x00]
        c[0] = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = b * 16
        return c

    @staticmethod
    def __adapt_right_color(color):

        if isinstance(color, list):
            color = rgb_to_hex(color)

        color = color.replace("#", '')

        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16
        c = [0x00, 0x00]
        c[0] = r  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c[1] = g * 16 + b
        return c

    def __get_cmd(self):
        return [self.__computer.fill_byte] * self.__computer.data_length

    def __save_line(self):

        if self.__save:
            legend = "__save_block, block={}".format(self.__block)

            cmd = self.__get_cmd()
            cmd[0] = self.__computer.start_byte
            cmd[1] = self.__computer.command_save_next
            cmd[2] = self.__block

            self.__commands.append(Command(legend, cmd))

    def __save_block(self):

        if self.__save:
            legend = "__save_block"

            cmd = self.__get_cmd()
            cmd[0] = self.__computer.start_byte
            cmd[1] = self.__computer.command_save

            self.__commands.append(Command(legend, cmd))
