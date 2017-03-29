#!/usr/bin/python3
#

#  Copyright (C) 2014-2015, 2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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


"""
    This file reads and writes the configuration files. It also stores the colors,
    zones and modes (fixed, morph, blink) that will be applied to the keyboard.
"""

import os
from traceback import format_exc

# local imports
from Computers import *
from Paths import *

profiles = {}


def LOAD_profiles(computer, profiles_path):
    global profiles
    profiles = {}

    # Load the existing profiles
    #
    if not os.path.exists(profiles_path):
        os.mkdir(profiles_path)
    else:
        files = os.listdir(profiles_path)

        for file in files:
            if file.endswith('.cfg'):
                LOAD_profile(computer, profiles_path + file)

    # Add the default profile
    #
    if len(profiles.keys()) <= 0:
        CREATE_default_profile(computer, profiles_path)


def LOAD_profile(computer, path):
    new_config = New(computer)
    new_config.path = path
    new_config.load(path)


def CREATE_default_profile(computer, profiles_path):
    config = New(computer)
    config.create_profile('Default', profiles_path + 'Default.cfg')
    config.save()


def GET_last_configuration():
    max = None
    profile_numb = 0
    profile_name = None

    for num, key in enumerate(sorted(profiles.keys())):

        profile = profiles[key]
        profile.update_time()

        if max is None or profile.time > max:
            max = profile.time
            profile_numb = num
            profile_name = profile.name

    return profile_numb, profile_name


class New:

    def __init__(self, computer):
        self.name = ''
        self.area = {}
        self.computer = computer
        self.speed = 65280
        self.time = None

    def create_profile(self, name, path, speed=False):
        self.name = name
        self.set_speed(speed)
        self.path = path

        for area in self.computer.regions.values():
            self.add_area(area)
            zone_data = ZoneData(
                area.regionId,
                self.computer.default_mode,
                area,
                self.computer.default_color,
                self.computer.default_color)
            self.add_zone(zone_data)

        profiles[self.name] = self

    def add_area(self, area):
        if not area.name in self.area.keys():
            self.area[area.name] = AreaData(area)
        else:
            print(
                "Warning: Duplicated area `{}`, `{}`".format(
                    area.name, self.area.keys()))

    def save(self):
        with open(self.path, encoding='utf-8', mode='wt') as f:
            f.write('name={0}\n'.format(self.name))
            f.write('computer={0}\n'.format(self.computer.name))
            f.write('speed={0}\n\n\n'.format(self.speed))

            for key in sorted(self.area.keys()):
                area = self.area[key]

                f.write('area={0}\n'.format(area.name))
                for zone_data in area:
                    f.write('mode={0}\n'.format(zone_data.mode))
                    f.write('color1={0}\n'.format(zone_data.color1))
                    f.write('color2={0}\n'.format(zone_data.color2))
                f.write('\n')

        self.update_time()

    def load(self, path):

        lines = []
        with open(path, encoding='utf-8', mode='rt') as f:
            lines = f.readlines()

        current_area, color1, color2, mode, = False, False, False, False

        # This variable is mostly to check for missing areas in the configuration file.
        # once everything has been imported, if something is missing the
        # default conf will be added.
        added_areas = []

        #
        # Parse the configuration file
        #
        for line in lines:
            if line.strip():
                variables = line.strip().split('=')

                if len(variables) == 2:

                    var_name = variables[0]
                    var_arg = variables[1]

                    if var_name == 'name':
                        if var_arg == '':
                            name = os.path.basename(path)
                        else:
                            name = var_arg

                        if name.endswith('.cfg'):
                            name = name[:-4]

                        self.name = name

                    elif var_name == 'speed':
                        self.set_speed(var_arg)

                    elif var_name == 'area':
                        area_name = var_arg

                        if area_name in self.computer.regions.keys():
                            added_areas.append(area_name)
                            current_area = self.computer.regions[area_name]
                            self.add_area(current_area)
                        else:
                            print(
                                "Warning: Wrong area name: {}, missing in dict: ".format(
                                    area_name, self.computer.regions))

                    elif var_name == 'type' or var_name == 'mode':
                        mode = var_arg

                    elif var_name == 'color' or var_name == 'color1':
                        color1 = var_arg

                    elif var_name == 'color2':
                        color2 = var_arg

                    if current_area and color1 and color2 and mode:
                        self.add_zone(
                            ZoneData(
                                current_area.regionId,
                                mode,
                                current_area,
                                color1,
                                color2))
                        color1, color2, mode = False, False, False

        #
        # Add the missing areas to the conf
        #
        for area_name in self.computer.regions.keys():
            if area_name not in added_areas:
                print(
                    "Warning: Missing area:{}, in profile: {}".format(
                        area_name, self.name))
                current_area = self.computer.regions[area_name]
                self.add_area(current_area)
                self.add_zone(ZoneData(current_area.regionId,
                                       self.computer.default_mode,
                                       current_area,
                                       self.computer.default_color,
                                       self.computer.default_color
                                       ))

        #
        # Add the configuration
        #
        profiles[self.name] = self

    def set_speed(self, speed):
        try:
            speed = int(speed)
            if speed >= 256 * 255:
                self.speed = 256 * 255
            elif speed <= 256:
                self.speed = 256
            else:
                self.speed = speed

        except Exception as e:
            self.speed = 1

            print("Warning: Configuration.py Error setting the speed.")
            print(format_exc())

    def modify_zone(self, zone, column, color1, color2, mode):
        zone_data = self.area[zone.name][column]
        zone_data.color1 = color1
        zone_data.color2 = color2
        zone_data.mode = mode

    def add_zone(self, zone_data):
        area_data = self.area[zone_data.name]
        area_data.add_zone(zone_data)

    def delete_zone(self, zone_data, column):
        try:
            area_data = self.area[zone_data.name]
            area_data.remove_zone(column)

        except Exception as e:
            print('Warning: column `{}`'.format(column))
            print(format_exc())

    def update_time(self):
        if os.path.exists(self.path):
            self.time = os.path.getmtime(self.path)


class AreaData(list):

    def __init__(self, area):
        self.area = area.name
        self.name = area.name
        self.description = area.description
        self.id = 0x01

    def add_zone(self, zone):
        el = zone
        el.id = self.id
        self.append(el)
        self.id += 1

    def remove_zone(self, column):
        object = self[column]
        self.remove(object)
        self.id = 0x01
        for zone in self:
            zone.id = self.id
            self.id += 1


class ZoneData:

    def __init__(self, id, mode=False, area=False, color1=False, color2=False):

        self.regionId = id
        self.mode = mode
        self.name = area.name
        self.description = area.description
        self.color1 = color1
        self.color2 = color2
