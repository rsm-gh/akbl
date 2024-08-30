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

_MISSING_ZONE_COLOR = "#0000FF"


class Theme:

    def __init__(self, computer) -> None:

        self.name = ''
        self.path = ''
        self._time = None
        self._computer = computer
        self.__areas = {}
        self.__speed = 1

    def get_speed(self) -> int:
        return self.__speed

    def set_speed(self, speed: int) -> None:
        """
           There are speed limits, but to avoid duplicated restrictions,
           they are applied in to the Constructor().
        """
        self.__speed = int(speed)

    def get_areas(self) -> tuple[Area]:
        return tuple([area for area in sorted(self.__areas.values(), key=lambda x: x.name)])

    def get_area_by_name(self, area_name: str) -> None | Area:

        if area_name in self.__areas:
            return self.__areas[area_name]

        return None

    def add_area(self, area: Area) -> None:
        if area.name not in self.__areas.keys():
            self.__areas[area.name] = area
        else:
            print_warning(f'Duplicated area "{area.name}", {self.__areas.keys()}')

    def modify_zone(self,
                    area_name: str,
                    column: int,
                    left_color: str,
                    right_color: str,
                    mode: str) -> None:
        zone = self.__areas[area_name].get_zone(column)
        zone.set_left_color(left_color)
        zone.set_right_color(right_color)
        zone.set_mode(mode)

    def delete_zone(self, area_name: str, column: int) -> None:
        area = self.__areas[area_name]
        area.remove_zone(column)

    def update_time(self) -> None:
        if os.path.exists(self.path):
            self._time = os.path.getmtime(self.path)

    def save(self) -> None:

        with open(self.path, encoding='utf-8', mode='w') as f:
            f.write(self.__str__())

        self.update_time()

    def __str__(self):

        theme_text = f'''
#############################################
#####            AKBL theme             #####
#############################################

name={self.name}
speed={self.__speed}
\n'''

        for area in sorted(self.__areas.values(), key=lambda x: x.name):
            theme_text += f'''
################### AREA #####################
area={area.name}
\n'''

            for zone in area.get_zones():
                theme_text += f'''
mode={zone.get_mode()}
left_color={zone.get_left_color()}
right_color={zone.get_right_color()}
'''

        return theme_text
