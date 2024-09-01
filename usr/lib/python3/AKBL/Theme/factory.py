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
from copy import deepcopy

from AKBL.Theme.Area import Area
from AKBL.Theme.AreaItem import AreaItem
from AKBL.utils import string_is_hex_color
from AKBL.console_printer import print_warning, print_debug
from AKBL.Computer.Computer import Computer
from AKBL.Theme.Theme import Theme
from AKBL.settings import _MISSING_ZONE_COLOR


def create_default_theme(computer: Computer, theme_dir: str = None) -> Theme:
    theme = Theme(computer)
    copy_theme(theme, os.path.join(theme_dir, 'Default.cfg'))
    theme.save()

    return theme


def load_theme_from_file(computer: Computer, path: str) -> Theme:
    print_debug('path="{}"'.format(path))

    theme = Theme(computer)
    theme.set_path(path)

    # Parse the configuration file
    #

    with open(path, encoding='utf-8', mode='rt') as f:
        lines = f.readlines()

    area = None
    left_color = ""
    right_color = ""
    mode = ""
    imported_areas = []
    supported_region_names = computer.get_regions_name()
    print_debug(f'supported_region_names={supported_region_names}', direct_output=True)

    for i, line in enumerate(lines, 1):

        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        line_data = line.split('=')
        if len(line_data) != 2:
            continue

        var_name = line_data[0]
        var_arg = line_data[1]

        match var_name:

            case 'speed':
                theme.set_speed(int(var_arg))

            case 'area':
                if var_arg in supported_region_names:
                    imported_areas.append(var_arg)
                    region = computer.get_region_by_name(var_arg)
                    area = Area(region)
                    theme.add_area(area)
                else:
                    area = None
                    print_warning(f"line {i}, area._name {var_arg} not listed on computer regions names")

            case 'mode':
                mode = var_arg
                if mode not in ('fixed', 'morph', 'blink'):
                    print_warning(
                        f'line {i}, wrong mode={mode} when importing theme. Using default mode={computer.default_mode}')
                    mode = computer.default_mode

            case 'left_color':
                if string_is_hex_color(var_arg):
                    left_color = var_arg
                else:
                    print_warning(f"line {i}, un-valid left_color value={var_arg}")

            case 'right_color':
                if string_is_hex_color(var_arg):
                    right_color = var_arg
                else:
                    print_warning(f"line {i}, un-valid right_color value={var_arg}")

        if area is not None and left_color != "" and right_color != "" and mode != "":
            print_debug(
                f'Area={area._name}, loading AreaItem mode={mode}, left_color={left_color}, right_color={right_color}',
                direct_output=True)

            areaitem = AreaItem(mode=mode,
                                left_color=left_color,
                                right_color=right_color)
            area.add_item(areaitem)

            left_color = ""
            right_color = ""
            mode = ""

    # Add areas in case they be missing
    #
    warning_text = ""
    for area_name in supported_region_names:
        if area_name not in imported_areas:
            region = computer.get_region_by_name(area_name)
            area = Area(region)

            theme.add_area(area)
            warning_text += f'Adding missing Area="{area_name}"\n'

            areaitem = AreaItem(mode=computer.default_mode,
                                left_color=_MISSING_ZONE_COLOR,
                                right_color=_MISSING_ZONE_COLOR)

            area.add_item(areaitem)

            warning_text += f'Adding AreaItem to the previous area, mode="{areaitem.get_mode()}" left_color="{areaitem.get_left_color()}" right_color="{areaitem.get_right_color()}"\n'

    if warning_text != "":
        print_warning(warning_text)

    return theme


def copy_theme(theme: Theme, path: str) -> Theme:
    new_theme = Theme(computer=theme._computer)
    new_theme.set_path(path)
    new_theme.set_speed(theme.get_speed())

    for area in theme.get_areas():
        new_theme.add_area(deepcopy(area))

    return new_theme


def get_theme_names(path):
    names = [filename[:-4] for filename in os.listdir(path) if filename.endswith('.cfg')]
    names.sort()
    #  names = [theme.get_name() for theme in _AVAILABLE_THEMES]
    #  names.sort()
    return names


def get_theme_by_name(computer: Computer,
                      themes_dir: str,
                      theme_name: str) -> None | Theme:
    if not theme_name.endswith('.cfg'):
        theme_name += ".cfg"

    theme_path = os.path.join(themes_dir, theme_name)

    if not os.path.exists(theme_path):
        return None

    return load_theme_from_file(computer, theme_path)


def get_last_theme_name(path) -> None | str:
    max_time = 0
    theme_name = None

    for filename in os.listdir(path):
        if filename.endswith(".cfg"):
            full_path = os.path.join(path, filename)
            theme_time = os.path.getmtime(full_path)
            if theme_time > max_time:
                max_time = theme_time
                theme_name = filename[:-4]

    return theme_name
