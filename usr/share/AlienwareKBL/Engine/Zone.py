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


class ZoneData:

    def __init__(self, left_color, right_color, mode, region_id=None):

        self.region_id = region_id
        self._mode = ''
        self._left_color = []
        self._right_color = []
        self._middle_color = []

    def set_region_id(self, value):
        self.regionId = value

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
            print('Warning: wrong `mode` on `set_mode` of ZoneData.')
