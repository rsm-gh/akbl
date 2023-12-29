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

from AKBL.utils import print_warning


class Zone:

    def __init__(self, left_color, right_color, mode, hex_id=1):

        self.__mode = ''
        self.__left_color = ''
        self.__right_color = ''
        self.__hex_id = hex_id

        self.set_mode(mode)
        self.set_left_color(left_color)
        self.set_right_color(right_color)

    def __str__(self):

        zone_description = '''
        hex_id={}
        mode={}
        left_color={}
        right_color={}
        '''.format(self.__hex_id,
                   self.__mode,
                   self.__left_color,
                   self.__right_color)

        return zone_description

    def set_hex_id(self, hex_id):
        self.__hex_id = hex_id

    def set_left_color(self, color):
        self.__left_color = color

    def set_right_color(self, color):
        self.__right_color = color

    def set_mode(self, mode):

        if mode == 'fixed':
            self.__mode = 'fixed'
        elif mode == 'morph':
            self.__mode = 'morph'
        elif mode == 'blink':
            self.__mode = 'blink'
        else:
            print_warning('wrong mode=`{}`'.format(mode))

    def get_hex_id(self):
        return self.__hex_id

    def get_mode(self):
        return self.__mode

    def get_left_color(self):
        return self.__left_color

    def get_right_color(self):
        return self.__right_color
