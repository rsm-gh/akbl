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

from Zone import ZoneData

class Region:

    def __init__(self, name, description, regionId, maxCommands, canBlink, canMorph, canLight, default_color, default_mode='fixed'):

        self.name = name
        self.description = description
        self.regionId = regionId
        self.canLight = canLight
        self.canBlink = canBlink
        self.canMorph = canMorph
        self.left_color = default_color
        self.right_color = default_color
        self.mode = default_mode
        self.maxCommands = maxCommands
        self.line = {1: ZoneData(self.left_color, self.right_color, self.mode)}

    def update_line(self, Id, mode=None, left_color=None, right_color=None):
        if Id in self.line:
            if mode:
                self.line[Id].mode = mode
            if left_color:
                self.line[Id].left_color = left_color
            if right_color:
                self.line[Id].right_color = right_color
            return True
        return False

    def add_line(self, Id, mode, left_color, right_color):
        Id = max(self.line.keys())
        if Id + 1 not in self.line:
            self.line[Id + 1] = ZoneData(left_color, right_color, mode)
            return True
        return False
