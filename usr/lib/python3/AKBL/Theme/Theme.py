#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
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

import os

from AKBL.console_printer import print_warning
from AKBL.Theme.Area import Area

from AKBL.console_printer import print_error


class Theme:

    def __init__(self, computer) -> None:

        self._computer = computer

        self.__name = ''
        self.__path = ''
        self.__areas = {}
        self.__speed = 1

    def __str__(self):

        theme_text = f'''
#############################################
#####            AKBL theme             #####
#############################################

speed={self.__speed}
\n'''

        for area in sorted(self.__areas.values(), key=lambda x: x._name):
            theme_text += f'''
################### AREA #####################
area={area._name}
\n'''

            for areaitem in area.get_items():
                theme_text += f'''
mode={areaitem.get_mode()}
left_color={areaitem.get_left_color()}
right_color={areaitem.get_right_color()}
'''

        return theme_text

    def add_area(self, area: Area) -> None:
        if area._name not in self.__areas:
            self.__areas[area._name] = area
        else:
            print_warning(f'Duplicated area "{area._name}"')

    def modify_areaitem(self,
                        area_name: str,
                        column: int,
                        left_color: str,
                        right_color: str,
                        mode: str) -> None:
        areaitem = self.__areas[area_name].get_item_at(column)
        areaitem.set_left_color(left_color)
        areaitem.set_right_color(right_color)
        areaitem.set_mode(mode)

    def delete_areaitem(self, area_name: str, column: int) -> None:
        area = self.__areas[area_name]
        area.remove_item_at(column)

    def save(self) -> None:

        with open(self.__path, encoding='utf-8', mode='w') as f:
            f.write(self.__str__())

    def get_name(self) -> str:
        return self.__name

    def get_speed(self) -> int:
        return self.__speed

    def get_areas(self) -> tuple[Area, ...]:
        return tuple([area for area in self.__areas.values()])

    def get_area_by_name(self, area_name: str) -> None | Area:
        if area_name in self.__areas:
            return self.__areas[area_name]

        return None

    def set_speed(self, speed: int) -> None:
        """
           There are speed limits, but to avoid duplicated restrictions,
           they are applied in to the Constructor().
        """
        self.__speed = int(speed)

    def set_path(self, path: str) -> None:

        if not path.endswith(".cfg"):
            path += ".cfg"

        name = os.path.basename(path)[:-4]
        if name == "":
            print_error(f"empty name for path={path}")
            return

        self.__path = path
        self.__name = name

    def get_path(self):
        return self.__path
