#!/usr/bin/python3
#

#  Copyright (C) 2014-2014 Rafael Senties Martinelli.
#                2011-2012 the pyAlienFX team.
#
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


class Region:

    def __init__(self,
                 name: str = None,
                 description: str = None,
                 hex_id: int = None,
                 max_commands: int = 0,
                 can_blink: bool = False,
                 can_morph: bool = False,
                 can_light: bool = False):
        self.name = name
        self.description = description
        self.hex_id = hex_id
        self.can_light = can_light
        self.can_blink = can_blink
        self.can_morph = can_morph
        self.max_commands = max_commands

    def __str__(self):
        return f'''
    name={self.name}
    description={self.description}
    hex_id={self.hex_id}
    can_light={self.can_light}
    can_blink={self.can_blink}
    can_morph={self.can_morph}
    max_commands={self.max_commands}
'''
