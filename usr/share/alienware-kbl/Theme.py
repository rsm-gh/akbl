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

import os
from traceback import format_exc

# Local imports
from Paths import *
from Computers import *
from Area import AreaData
from Zone import ZoneData

INSTANCES_DIC = {}


def LOAD_profiles(computer, theme_path):
    global INSTANCES_DIC
    INSTANCES_DIC = {}

    # Load the existing INSTANCES_DIC
    #
    if not os.path.exists(theme_path):
        os.mkdir(theme_path)
    else:
        files = os.listdir(theme_path)

        for file in files:
            if file.endswith('.cfg'):
                LOAD_profile(computer, theme_path + file)

    # Add the default profile
    #
    if len(INSTANCES_DIC.keys()) <= 0:
        CREATE_default_profile(computer, theme_path)


def LOAD_profile(computer, path):
    new_config = Theme(computer)
    new_config.path = path
    new_config.load(path)


def CREATE_default_profile(computer, theme_path):
    config = Theme(computer)
    config.create_profile('Default', theme_path + 'Default.cfg')
    config.save()


def GET_last_configuration():
    max = None
    profile_numb = 0
    profile_name = None

    for num, key in enumerate(sorted(INSTANCES_DIC.keys())):

        profile = INSTANCES_DIC[key]
        profile.update_time()

        if max is None or profile.time > max:
            max = profile.time
            profile_numb = num
            profile_name = profile.name

    return profile_numb, profile_name

class Theme:

    def __init__(self, computer):
        self.name = ''
        self.computer = computer
        self.speed = 65280
        self.time = None
        self._area_instances_dic = {}

    def create_profile(self, name, path, speed=False):
        self.name = name
        self.set_speed(speed)
        self.path = path

        for area in self.computer.regions.values():
            zone_data = ZoneData(region_id=area.regionId,
                                 mode=self.computer.default_mode,
                                 left_color=self.computer.default_color,
                                 right_color=self.computer.default_color)
            area.add_zone_data(zone_data)
            self.add_area(area)

        INSTANCES_DIC[self.name] = self

    def get_areas(self):
        return self._area_instances_dic

    def add_area(self, area_data):
        if not area_data.name in self._area_instances_dic.keys():
            self._area_instances_dic[area_data.name] = area_data
        else:
            print("Warning: Duplicated area `{}`, `{}`".format(area_data.name, self._area_instances_dic.keys()))

    def save(self):
        with open(self.path, encoding='utf-8', mode='wt') as f:
            f.write('name={0}\n'.format(self.name))
            f.write('computer={0}\n'.format(self.computer.name))
            f.write('speed={0}\n\n\n'.format(self.speed))

            for key in sorted(self._area_instances_dic.keys()):
                area = self._area_instances_dic[key]

                f.write('area={0}\n'.format(area.name))
                for zone_data in area:
                    f.write('mode={0}\n'.format(zone_data.get_mode()))
                    f.write('left_color={0}\n'.format(zone_data.get_left_color()))
                    f.write('right_color={0}\n'.format(zone_data.get_right_color()))
                f.write('\n')

        self.update_time()

    def load(self, path):

        lines = []
        with open(path, encoding='utf-8', mode='rt') as f:
            lines = f.readlines()

        area_found, color1, color2, mode, = False, False, False, False

        imported_areas = []
        supported_areas_ids = self.computer.regions.keys()

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
                        area_id = var_arg

                        if area_id in supported_areas_ids:
                            area_found=True
                            imported_areas.append(area_id)
                            region_object = self.computer.regions[area_id]
                            area = AreaData(name=region_object.name, description=region_object.description)
                            self.add_area(area)
                        else:
                            area_found=False
                            print("Warning: area name `{}` not listed on computer regions.".format(area_id))

                    elif var_name in ('type','mode'):
                        mode = var_arg

                    elif var_name in ('color','color1','left_color'):
                        color1 = var_arg

                    elif var_name in ('color2','right_color'):
                        color2 = var_arg

                    if area_found and color1 and color2 and mode:
                        zone_data=ZoneData(region_id=region_object.regionId,
                                           mode=mode,
                                           color1=color1,
                                           color2=color2)

                        area.add_zone_data(zone_data)

                        color1, color2, mode = False, False, False

        # Add areas in case they be missing
        #
        for area_id in supported_areas_ids:
            if area_id not in imported_areas:

                region_object = self.computer.regions[area_id]
                area = AreaData(name=region_object.name, description=region_object.description)

                zone_data = ZoneData(region_object.regionId,
                                     self.computer.default_mode,
                                     self.computer.default_color,
                                     self.computer.default_color)
                area.add_zone_data(zone_data)

                self.add_area(area)
                print("Warning: missing area `{}` at the theme `{}`.".format(area_name, self.name))

        #
        # Add the configuration
        #
        INSTANCES_DIC[self.name] = self

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
        zone_data = self._area_instances_dic[zone.name][column]
        zone_data.color1 = color1
        zone_data.color2 = color2
        zone_data.mode = mode

    def delete_zone(self, zone_data, column):
        try:
            area_data = self._area_instances_dic[zone_data.name]
            area_data.remove_zone(column)

        except Exception as e:
            print('Warning: column `{}`'.format(column))
            print(format_exc())

    def update_time(self):
        if os.path.exists(self.path):
            self.time = os.path.getmtime(self.path)
