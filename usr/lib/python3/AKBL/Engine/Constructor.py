#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
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

from AKBL.utils import rgb_to_hex
from AKBL.Computer import Computer
from AKBL.Engine.Command import Command
from AKBL.console_printer import print_warning


class Constructor:

    def __init__(self,
                 computer: Computer,
                 save: bool = False,
                 block: int = 1) -> None:

        self.__computer = computer
        self.__commands = []
        self.__block = block
        self.__hex_id = 1
        self.__save = save

    def __str__(self) -> str:
        return "Constructor: computer.name={}, hex_id={}, block={}, _save={}".format(self.__computer.name,
                                                                                     self.__hex_id,
                                                                                     self.__block,
                                                                                     self.__save)

    def __iter__(self):
        for command in self.__commands:
            yield command

    def clear(self) -> None:
        self.__commands.clear()
        self.__hex_id = 1

    def get_first_command(self) -> None | int:

        if len(self.__commands) > 0:
            return self.__commands[0]

        return None

    def add_light_zone(self, area_hex_id: int, color: list[int] | str) -> None:
        legend = '''add_light_zone: left_color={}, hex_id={}'''.format(color, area_hex_id)

        self.__save_line()
        self.__add_zone(area_hex_id=area_hex_id,
                        left_color=color,
                        right_color=None,
                        legend=legend,
                        cmd_color_type=self.__computer.command_set_color)

    def add_blink_zone(self, area_hex_id: int, color: list[int] | str) -> None:
        legend = "add_blink_zone:color={}, hex_id={}".format(color, area_hex_id)
        self.__add_zone(area_hex_id=area_hex_id,
                        left_color=color,
                        right_color=None,
                        legend=legend,
                        cmd_color_type=self.__computer.command_set_blink_color)

    def add_morph_zone(self,
                       area_hex_id: int,
                       left_color: list[int] | str,
                       right_color: list[int] | str) -> None:

        legend = '''add_morph_zone: left_color={}, right_color={}, hex_id={}'''.format(left_color,
                                                                                       right_color,
                                                                                       area_hex_id)

        self.__add_zone(area_hex_id=area_hex_id,
                        left_color=left_color,
                        right_color=right_color,
                        legend=legend,
                        cmd_color_type=self.__computer.command_set_morph_color)

    def set_block(self, save: bool, block: int) -> None:
        self.__save = save
        self.__block = block
        self.__hex_id = 1

    def set_speed(self, speed: int) -> None:

        speed = int(speed)  # Only for caution, in case of int not provided

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
        cmd[3] = speed

        self.__commands.append(Command(legend, cmd))

    def set_get_status(self) -> None:

        legend = "set_get_status"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_get_status

        self.__commands.append(Command(legend, cmd))

    def set_reset_area(self, computer_command=None) -> None:

        match computer_command:
            case None | self.__computer.reset_all_lights_on:
                computer_command = self.__computer.reset_all_lights_on
                legend = "reset, command=RESET_ALL_LIGHTS_ON\n"

            case self.__computer.reset_all_lights_off:
                legend = "reset, command=RESET_ALL_LIGHTS_OFF\n"

            case self.__computer.reset_touch_controls:
                legend = "reset, command=RESET_TOUCH_CONTROLS\n"

            case _:
                legend = "reset, command=UNKNOWN COMMAND !!\n"
                print_warning("Wrong command={}".format(computer_command))

        self.__save_line()

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_reset
        cmd[2] = computer_command

        self.__commands.append(Command(legend, cmd))

    def set_end_colors_line(self) -> None:

        self.__save_line()

        legend = "end_colors_line\n"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_loop_block_end

        self.__hex_id += 1
        self.__commands.append(Command(legend, cmd))

    def set_end_block_line(self) -> None:

        self.__save_block()

        legend = "end_block_line\n\n"

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = self.__computer.command_transmit_execute

        self.__commands.append(Command(legend, cmd))

    def __add_zone(self,
                   area_hex_id: int,
                   left_color: str,
                   right_color: None | str,
                   legend: str,
                   cmd_color_type: int) -> None:

        self.__save_line()

        parsed_area_hex_id = self.__adapt_area_hex_id(area_hex_id)
        adapted_left_color = self.__adapt_left_color(left_color)

        cmd = self.__get_cmd()
        cmd[0] = self.__computer.start_byte
        cmd[1] = cmd_color_type
        cmd[2] = self.__hex_id
        cmd[3] = parsed_area_hex_id[0]
        cmd[4] = parsed_area_hex_id[1]
        cmd[5] = parsed_area_hex_id[2]
        cmd[6] = adapted_left_color[0]

        if right_color is None:
            cmd[7] = adapted_left_color[1]
        else:
            adapted_right_color = self.__adapt_right_color(right_color)
            cmd[7] = adapted_left_color[1] + adapted_right_color[0]
            cmd[8] = adapted_right_color[1]

        self.__commands.append(Command(legend, cmd))

    @staticmethod
    def __adapt_area_hex_id(area_hex_id: int) -> tuple[int, int, int]:
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
        # pyALienFX: takes the two first digits
        value_0 = area_hex_id // 65536

        # pyALienFX: takes the four first digits and remove the two first digits
        value_1 = area_hex_id // 256 - value_0 * 256

        # pyALienFX: same but remove the first 4 digits
        value_2 = area_hex_id - value_0 * 65536 - value_1 * 256

        return value_0, value_1, value_2

    def __adapt_left_color(self, color: list[int] | str) -> tuple[int, int]:

        r, g, b = self.__adapt_color(color)

        c0 = r * 16 + g  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c1 = b * 16
        return c0, c1

    def __adapt_right_color(self, color: list[int] | str) -> tuple[int, int]:

        r, g, b = self.__adapt_color(color)
        c0 = r  # if r = 0xf > r*16 = 0xf0 > and b = 0xc r*16 + b 0xfc
        c1 = g * 16 + b
        return c0, c1

    @staticmethod
    def __adapt_color(color: list[int] | str) -> tuple[int, int, int]:
        if isinstance(color, list):
            color = rgb_to_hex(color)

        color = color.replace("#", '')

        r = int(color[0:2], 16) // 16
        g = int(color[2:4], 16) // 16
        b = int(color[4:6], 16) // 16

        return r, g, b

    def __get_cmd(self) -> list[int]:
        return [self.__computer.fill_byte] * self.__computer.data_length

    def __save_line(self) -> None:

        if self.__save:
            legend = "__save_block, block={}".format(self.__block)

            cmd = self.__get_cmd()
            cmd[0] = self.__computer.start_byte
            cmd[1] = self.__computer.command_save_next
            cmd[2] = self.__block

            self.__commands.append(Command(legend, cmd))

    def __save_block(self) -> None:

        if self.__save:
            legend = "__save_block"

            cmd = self.__get_cmd()
            cmd[0] = self.__computer.start_byte
            cmd[1] = self.__computer.command_save

            self.__commands.append(Command(legend, cmd))
