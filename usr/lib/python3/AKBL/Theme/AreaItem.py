#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
#                2011-2012 the pyAlienFX team.
#
#  AKBL is free software; you can redistribute it and/or modify
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

from utils import string_is_hex_color
from console_printer import print_warning


class AreaItem:

    def __init__(self,
                 left_color: str,
                 right_color: str,
                 mode: str,
                 hex_id: int = 1):

        self.__mode = ''
        self.__left_color = ''
        self.__right_color = ''
        self.__hex_id = hex_id

        self.set_mode(mode)
        self.set_left_color(left_color)
        self.set_right_color(right_color)

    def __str__(self):
        return f'''
        hex_id={self.__hex_id}
        mode={self.__mode}
        left_color={self.__left_color}
        right_color={self.__right_color}
        '''

    def set_hex_id(self, hex_id: int) -> None:
        if hex_id > 0:
            self.__hex_id = hex_id
        else:
            print_warning(f"wrong hex_id={hex_id}")

    def set_left_color(self, color: str) -> None:
        if string_is_hex_color(color):
            self.__left_color = color
        else:
            print_warning(f"wrong color={color}")

    def set_right_color(self, color: str) -> None:
        if string_is_hex_color(color):
            self.__right_color = color
        else:
            print_warning(f"wrong color={color}")

    def set_mode(self, mode: str) -> None:
        match mode:
            case 'fixed' | 'morph' | 'blink':
                self.__mode = mode
            case _:
                print_warning(f"wrong mode='{mode}'")

    def get_hex_id(self) -> int:
        return self.__hex_id

    def get_mode(self) -> str:
        return self.__mode

    def get_left_color(self) -> str:
        return self.__left_color

    def get_right_color(self) -> str:
        return self.__right_color
