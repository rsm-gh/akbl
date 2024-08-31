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

from copy import copy

from AKBL.Theme.Zone import Zone
from AKBL.Computer.Region import Region


class Area(Region):

    def __init__(self, region) -> None:
        super().__init__(name=region._name,
                         description=region._description,
                         hex_id=region._hex_id,
                         can_light=region._can_light,
                         can_blink=region._can_blink,
                         can_morph=region._can_morph,
                         max_commands=region._max_commands)

        self.__current_zone_hex_id = self._hex_id
        self.__zones = []

    def __str__(self) -> str:

        zones_description = ""
        for zone in self.__zones:
            zones_description += str(zone)

        return f'''
    name={self._name}
    description={self._description}
    hex_id={self._hex_id}
    current_zone_hex_id={self.__current_zone_hex_id}
    can_light={self._can_light}
    can_blink={self._can_blink}
    can_morph={self._can_morph}
    max_commands={self._max_commands}
    zones:
{zones_description}
'''

    def add_zone(self, zone: Zone) -> None:
        zone.set_hex_id(self.__current_zone_hex_id)
        self.__zones.append(zone)
        self.__current_zone_hex_id += 1

    def remove_zone(self, column_index: int) -> None:
        zone = self.__zones[column_index]
        self.__zones.remove(zone)
        self.__current_zone_hex_id = self._hex_id
        for zone in self.__zones:
            zone.set_hex_id(self.__current_zone_hex_id)
            self.__current_zone_hex_id += 1

    def get_zone(self, column_index: int) -> Zone:
        return self.__zones[column_index]

    def get_zones(self) -> list[Zone]:
        return copy(self.__zones)
