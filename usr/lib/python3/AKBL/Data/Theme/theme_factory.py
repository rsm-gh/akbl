#!/usr/bin/python3
#

#  Copyright (C) 2014-2018  Rafael Senties Martinelli
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

from AKBL.utils import print_warning, print_debug, string_is_hex_color
from AKBL.Data.Theme.Theme import Theme, _MISSING_ZONE_COLOR
from AKBL.Data.Theme.Area import Area
from AKBL.Data.Theme.Zone import Zone

_AVAILABLE_THEMES = {}

def get_theme_by_name(name):
    return _AVAILABLE_THEMES[name]

def LOAD_profiles(computer, folder_path):

    global _AVAILABLE_THEMES
    _AVAILABLE_THEMES = {}

    # Load the existing _AVAILABLE_THEMES
    #
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        files = os.listdir(folder_path)

        for file_name in files:
            if file_name.endswith('.cfg'):
                load_from_file(folder_path + file_name, computer)

    
    # Add the default profile
    #
    if len(_AVAILABLE_THEMES.keys()) <= 0:
        CREATE_default_profile(computer, folder_path)


def CREATE_default_profile(computer, theme_path):
    theme = Theme(computer)
    copy_theme(theme, 'Default', theme_path + 'Default.cfg')
    theme.save()

def GET_last_configuration():
    max_time = None
    profile_numb = 0
    profile_name = None

    for num, key in enumerate(sorted(_AVAILABLE_THEMES.keys())):

        profile = _AVAILABLE_THEMES[key]
        profile.update_time()

        if max_time is None or profile._time > max_time:
            max_time = profile._time
            profile_numb = num
            profile_name = profile.name

    return profile_numb, profile_name


def load_from_file(path, computer):
    
    print_debug('path=`{}`'.format(path))
    
    with open(path, encoding='utf-8', mode='rt') as f:
        lines = f.readlines()

    area_found, left_color, right_color, mode, = False, False, False, False

    imported_areas = []
    supported_region_names = computer.get_regions_name()
    #print_debug('supported_region_names=`{}`'.format(supported_region_names))


    theme = Theme(computer)
    theme.path = path

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

                    theme.name = name

                elif var_name == 'speed':
                    theme.set_speed(var_arg)

                elif var_name == 'area':
                    area_name = var_arg

                    if area_name in supported_region_names:
                        area_found=True
                        imported_areas.append(area_name)
                        region = computer.get_region_by_name(area_name)
                        area = Area(region)                         
                        theme.add_area(area)
                    else:
                        area_found=False
                        print_warning("area.name `{}` not listed on computer regions names".format(area_name))

                elif var_name in ('type','mode'):  # `type`is to give support to old themes
                    mode = var_arg
                    if mode not in ('fixed', 'morph', 'blink'):
                        default_mode = computer.DEFAULT_MODE
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

            region = computer.get_region_by_name(area_name)
            area = Area(region)

            zone = Zone(mode=computer.DEFAULT_MODE,
                        left_color=_MISSING_ZONE_COLOR,
                        right_color=_MISSING_ZONE_COLOR)
            
            area.add_zone(zone)
            theme.add_area(area)
            print_warning("missing area.name=`{}` on theme=`{}`".format(area_name, theme.name))
            print_debug('adding Zone to the missing Area, mode=`{}`, left_color=`{}`, right_color=`{}`'.format(zone.get_mode(), zone.get_left_color(), zone.get_right_color()))


    print_debug(theme)

    #
    # Add the configuration
    #
    _AVAILABLE_THEMES[theme.name] = theme
    
    
def copy_theme(theme, name, path, speed=1):
    theme.name = name
    theme.set_speed(speed)
    theme.path = path

    for region in theme._computer.get_regions():
        
        area = Area(region)
        zone = Zone(mode=theme._computer.DEFAULT_MODE, 
                    left_color=_MISSING_ZONE_COLOR, 
                    right_color=_MISSING_ZONE_COLOR)

        area.add_zone(zone)
        theme.add_area(area)

    _AVAILABLE_THEMES[theme.name] = theme