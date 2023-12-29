#!/usr/bin/python3
#

#  Copyright (C) 2014-2018 Rafael Senties Martinelli.
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


from AKBL.Data.Computer.Region import Region


class Area(Region):

    def __init__(self, region):
        super().__init__(name=region.name,
                         description=region.description,
                         hex_id=region.hex_id,
                         can_light=region.can_light,
                         can_blink=region.can_blink,
                         can_morph=region.can_morph,
                         max_commands=region.max_commands)

        self.__current_zone_hex_id = self.hex_id
        self.__zones = []

    def __str__(self):

        zones_description = ""
        for zone in self.__zones:
            zones_description += str(zone)

        area_description = '''
    name={}
    description={}
    hex_id={}
    current_zone_hex_id={}
    can_light={}
    can_blink={}
    can_morph={}
    max_commands={}
    zones:
{}
'''.format(self.name,
           self.description,
           self.hex_id,
           self.__current_zone_hex_id,
           self.can_light,
           self.can_blink,
           self.can_morph,
           self.max_commands,
           zones_description)

        return area_description

    def get_zone(self, column_index):
        return self.__zones[column_index]

    def get_zones(self):
        return self.__zones

    def get_number_of_zones(self):
        return len(self.__zones)

    def add_zone(self, zone):
        zone.set_hex_id(self.__current_zone_hex_id)
        self.__zones.append(zone)
        self.__current_zone_hex_id += 1

    def remove_zone(self, column_index):
        zone = self.__zones[column_index]
        self.__zones.remove(zone)
        self.__current_zone_hex_id = self.hex_id
        for zone in self.__zones:
            zone.set_hex_id(self.__current_zone_hex_id)
            self.__current_zone_hex_id += 1
