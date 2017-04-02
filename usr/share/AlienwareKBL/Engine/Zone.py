#!/usr/bin/python3
#

#  Copyright (C) 2014-2015, 2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
#                2011-2012  the pyAlienFX team
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


class Zone:

    def __init__(self, left_color, right_color, mode, hex_id=0x01):

        self._mode = ''
        self._left_color = []
        self._right_color = []
        self._middle_color = []
        self._hex_id = hex_id

    def set_hex_id(self, hex_id):
        self._hex_id = hex_id

    def set_region_id(self, value):
        self.region_id = value

    def get_region_id(self):
        return self._region_id

    def get_mode(self):
        return self._mode

    def get_left_color(self):
        return self._left_color

    def get_right_color(self):
        return self._right_color

    def set_color(self, color, side):

        if isinstance(color, str):
            color = hex_to_rgb(color)

        if side == 'left':
            self._left_color = normalize_rgb(color)
        elif side == 'right':
            self._right_color = normalize_rgb(color)
        else:
            print("Warning: wrong `side` on `set_color`", side)

        if self._left_color and self._right_color:
            self._middle_color = middle_rgb_color(self._left_color, self._right_color)

    def set_mode(self, mode):

        if mode == 'fixed':
            self._mode = 'fixed'
        elif mode == 'morph':
            self._mode = 'morph'
        elif mode == 'blink':
            self._mode = 'blink'
        else:
            print('Warning: wrong `mode` on `set_mode` of Zone.')
