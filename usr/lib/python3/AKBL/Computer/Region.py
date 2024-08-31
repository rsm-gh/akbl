#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
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
                 name: str,
                 description: str,
                 hex_id: int,
                 max_commands: int,
                 can_blink: bool,
                 can_morph: bool,
                 can_light: bool):
        self._name = name
        self._description = description
        self._hex_id = hex_id
        self._can_light = can_light
        self._can_blink = can_blink
        self._can_morph = can_morph
        self._max_commands = max_commands

    def __str__(self):
        return f'''
    name={self._name}
    description={self._description}
    hex_id={self._hex_id}
    can_light={self._can_light}
    can_blink={self._can_blink}
    can_morph={self._can_morph}
    max_commands={self._max_commands}
'''
