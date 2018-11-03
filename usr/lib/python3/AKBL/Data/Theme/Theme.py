#!/usr/bin/python3
#

#  Copyright (C) 2014-2018  RSM
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
from copy import copy

from AKBL.utils import print_warning, print_debug, string_is_hex_color
from AKBL.Data.Theme.Area import Area
from AKBL.Data.Theme.Zone import Zone

AVAILABLE_THEMES = {}

_MISSING_ZONE_COLOR="#0000FF"

def get_theme_by_name(name):
    return AVAILABLE_THEMES[name]

def LOAD_profiles(computer, theme_path):

    global AVAILABLE_THEMES
    AVAILABLE_THEMES = {}

    # Load the existing AVAILABLE_THEMES
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
    if len(AVAILABLE_THEMES.keys()) <= 0:
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
    max_time = None
    profile_numb = 0
    profile_name = None

    for num, key in enumerate(sorted(AVAILABLE_THEMES.keys())):

        profile = AVAILABLE_THEMES[key]
        profile.update_time()

        if max_time is None or profile._time > max_time:
            max_time = profile._time
            profile_numb = num
            profile_name = profile.name

    return profile_numb, profile_name

class Theme:

    def __init__(self, computer):

        self.name = ''
        self._time = None
        
        self.__areas = {}
        self._computer = copy(computer)
        
        self.__speed = 1
        self.set_speed(self._computer.DEFAULT_SPEED)

    def __str__(self):
        
        theme_text='''
#############################################
##### Alienware-KBL configuration theme #####
#############################################

name={}
speed={}
\n'''.format(self.name, self.__speed)
            
        for area in sorted(self.__areas.values(), key=lambda x: x.name):
            theme_text+='''
********************************************
area={}

'''.format(area.name)
            
            for zone in area.get_zones():
                theme_text+='''
mode={}
left_color={}
right_color={}
'''.format(zone.get_mode(), zone.get_left_color(), zone.get_right_color())
        
        return theme_text
        
    def get_areas(self):
        return (area for area in sorted(self.__areas.values(), key=lambda x: x.name))

    def get_area_by_name(self, area_name):
        
        if area_name in self.__areas.keys():
            return self.__areas[area_name]

        return None

    def get_speed(self):
        return self.__speed

    def set_speed(self, speed):
        """
           There are speed limits but in order to avoid duplicated restrictions,
           they went applied in to the Constructor(). 
        """
        self.__speed = int(speed)
        
    def create_profile(self, name, path, speed=False):
        self.name = name
        self.set_speed(speed)
        self.path = path

        for region in self._computer.get_regions():
            
            area = Area(region)
            zone = Zone(mode=self._computer.DEFAULT_MODE, 
                        left_color=_MISSING_ZONE_COLOR, 
                        right_color=_MISSING_ZONE_COLOR)

            area.add_zone(zone)
            self.add_area(area)

        AVAILABLE_THEMES[self.name] = self

    def add_area(self, area):
        if not area.name in self.__areas.keys():
            self.__areas[area.name] = area
        else:
            print_warning("Duplicated area `{}`, `{}`".format(area.name, self.__areas.keys()))

    def modify_zone(self, area_name, column, left_color, right_color, mode):
        zone = self.__areas[area_name].get_zone(column)
        zone.set_left_color(left_color)
        zone.set_right_color(right_color)
        zone.set_mode(mode)

    def delete_zone(self, area_name, column):
        area = self.__areas[area_name]
        area.remove_zone(column)

    def update_time(self):
        if os.path.exists(self.path):
            self._time = os.path.getmtime(self.path)

    def save(self):
        
        with open(self.path, encoding='utf-8', mode='w') as f:
            f.write(self.__str__())
            

        self.update_time()

    def load(self, path):

        print_debug('path=`{}`'.format(path))
        
        with open(path, encoding='utf-8', mode='rt') as f:
            lines = f.readlines()

        area_found, left_color, right_color, mode, = False, False, False, False

        imported_areas = []
        supported_region_names = self._computer.get_regions_name()
        #print_debug('supported_region_names=`{}`'.format(supported_region_names))

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

                        if area_name in supported_region_names:
                            area_found=True
                            imported_areas.append(area_name)
                            region = self._computer.get_region_by_name(area_name)
                            area = Area(region)                         
                            self.add_area(area)
                        else:
                            area_found=False
                            print_warning("area.name `{}` not listed on computer regions names".format(area_name))

                    elif var_name in ('type','mode'):  # `type`is to give support to old themes
                        mode = var_arg
                        if mode not in ('fixed', 'morph', 'blink'):
                            default_mode = self._computer.DEFAULT_MODE
                            print_warning('wrong mode=`{}` when importing theme. Using default mode=`{}`'.format(mode, default_mode))
                            mode = default_mode

                    elif var_name in ('color','color1','left_color'):  # `color` & `color1`are to give support to old themes
                        
                        if string_is_hex_color(var_arg):
                            left_color = var_arg
                        else:
                            
                            if area_found:
                                area_name = area.name
                            else:
                                area_name = "?"
                        
                            print_warning("Wrong left hex_color={} for area={}, the default hex_color= will be used instead.".format(left_color, 
                                                                                                                                     area_name, 
                                                                                                                                     _MISSING_ZONE_COLOR))
                            left_color = _MISSING_ZONE_COLOR

                    elif var_name in ('color2','right_color'):  # `color2` is to give support to old themes

                        if string_is_hex_color(var_arg):
                            right_color = var_arg
                        else:
 
                            if area_found:
                                area_name = area.name
                            else:
                                area_name = "?"                           
                            
                            print_warning("Wrong left hex_color={} for area={}, the default hex_color={} will be used instead.".format(right_color,
                                                                                                                                       area_name,
                                                                                                                                       _MISSING_ZONE_COLOR))
                            right_color = _MISSING_ZONE_COLOR

                    if area_found and left_color and right_color and mode:
                        
                        #print_debug('adding Zone to Area, mode=`{}`, left_color=`{}`, right_color=`{}`'.format(mode, left_color, right_color))
                        
                        zone=Zone(mode=mode, left_color=left_color, right_color=right_color)
                        area.add_zone(zone)

                        left_color, right_color, mode = False, False, False

        # Add areas in case they be missing
        #
        for area_name in supported_region_names:
            if area_name not in imported_areas:

                region = self._computer.get_region_by_name(area_name)
                area = Area(region)

                zone = Zone(mode=self._computer.DEFAULT_MODE,
                            left_color=_MISSING_ZONE_COLOR,
                            right_color=_MISSING_ZONE_COLOR)
                
                area.add_zone(zone)
                self.add_area(area)
                print_warning("missing area.name=`{}` on theme=`{}`".format(area_name, self.name))
                print_debug('adding Zone to the missing Area, mode=`{}`, left_color=`{}`, right_color=`{}`'.format(zone.get_mode(), zone.get_left_color(), zone.get_right_color()))


        print_debug(self)

        #
        # Add the configuration
        #
        AVAILABLE_THEMES[self.name] = self
