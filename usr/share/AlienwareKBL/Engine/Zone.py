#!/usr/bin/python3
#

#  Copyright (C) 2014-2015, 2017  Rafael Senties Martinelli 
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

import sys

sys.path.insert(0, "/usr/share/AlienwareKBL")
from utils import print_warning, hex_to_rgb, rgb_to_hex, middle_rgb_color

class Zone:

    def __init__(self, left_color, right_color, mode, hex_id=1):

        self._mode = ''
        self._left_color = ''
        self._right_color = ''
        self._hex_id = hex_id

        self.set_mode(mode)
        self.set_color(left_color, 'left')
        self.set_color(right_color, 'right')

    def __str__(self):
        
        zone_description='''
        hex_id={}
        mode={}
        left_color={}
        right_color={}
        '''.format(self._hex_id, self._mode, self._left_color, self._right_color)
        
        return zone_description

    def set_hex_id(self, hex_id):
        self._hex_id = hex_id

    def get_hex_id(self):
        return self._hex_id

    def get_mode(self):
        return self._mode

    def get_left_color(self):
        return self._left_color

    def get_right_color(self):
        return self._right_color

    def set_color(self, color, side):

        if side == 'left':
            self._left_color = color
        elif side == 'right':
            self._right_color = color
        else:
            print_warning("wrong side=`{}`", side)

    def set_mode(self, mode):

        if mode == 'fixed':
            self._mode = 'fixed'
        elif mode == 'morph':
            self._mode = 'morph'
        elif mode == 'blink':
            self._mode = 'blink'
        else:
            print_warning('wrong mode=`{}`'.format(mode))
