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


class AreaData(list):

    def __init__(self, name, description, id=0x01):

        self.name = name
        self.description = description
        self.id = id

    def get_number_of_zones(self):
        return len(self)

    def add_zone_data(self, zone_data):
        zone_data.set_region_id(self.id)
        self.append(zone_data)
        self.id += 1

    def remove_zone(self, column):
        object = self[column]
        self.remove(object)
        self.id = 0x01
        for zone in self:
            zone.id = self.id
            self.id += 1
