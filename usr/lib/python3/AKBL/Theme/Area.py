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

from Theme.AreaItem import AreaItem
from Computer.Region import Region


class Area(Region):

    def __init__(self, region) -> None:
        super().__init__(name=region._name,
                         description=region._description,
                         hex_id=region._hex_id,
                         can_light=region._can_light,
                         can_blink=region._can_blink,
                         can_morph=region._can_morph,
                         max_commands=region._max_commands)

        self.__current_areaitem_hex_id = self._hex_id
        self.__area_items = []

    def __str__(self) -> str:

        area_items_description = ""
        for areaitem in self.__area_items:
            area_items_description += str(areaitem)

        return f'''
    name={self._name}
    description={self._description}
    hex_id={self._hex_id}
    current_areaitem_hex_id={self.__current_areaitem_hex_id}
    can_light={self._can_light}
    can_blink={self._can_blink}
    can_morph={self._can_morph}
    max_commands={self._max_commands}
    area_items:
{area_items_description}
'''

    def add_item(self, areaitem: AreaItem) -> None:
        areaitem.set_hex_id(self.__current_areaitem_hex_id)
        self.__area_items.append(areaitem)
        self.__current_areaitem_hex_id += 1

    def remove_item_at(self, column_index: int) -> None:
        areaitem = self.__area_items[column_index]
        self.__area_items.remove(areaitem)
        self.__current_areaitem_hex_id = self._hex_id
        for areaitem in self.__area_items:
            areaitem.set_hex_id(self.__current_areaitem_hex_id)
            self.__current_areaitem_hex_id += 1

    def get_item_at(self, column_index: int) -> AreaItem:
        return self.__area_items[column_index]

    def get_items(self) -> list[AreaItem]:
        return copy(self.__area_items)
