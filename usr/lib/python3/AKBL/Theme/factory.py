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

from AKBL.Theme.Area import Area
from AKBL.Theme.AreaItem import AreaItem
from AKBL.utils import string_is_hex_color
from AKBL.console_printer import print_warning, print_debug
from AKBL.Computer.Computer import Computer
from AKBL.Theme.Theme import Theme
from AKBL.settings import _MISSING_ZONE_COLOR

_AVAILABLE_THEMES = []  # It can not be a dictionary, because the theme name can change.


def get_theme_names():
    names = [theme.get_name() for theme in _AVAILABLE_THEMES]
    names.sort()
    return names


def get_theme_by_name(name) -> None | Theme:
    for theme in _AVAILABLE_THEMES:
        if theme.get_name() == name:
            return theme

    return None


def load_themes(computer: Computer, folder_path: str = None) -> Theme:
    global _AVAILABLE_THEMES
    _AVAILABLE_THEMES = []

    # Load the existing _AVAILABLE_THEMES
    #
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        files = os.listdir(folder_path)

        for file_name in files:
            if file_name.endswith('.cfg'):
                theme = load_theme_from_file(computer, folder_path + file_name)

                if get_theme_by_name(theme.get_name()) is None:
                    _AVAILABLE_THEMES.append(theme)
                else:
                    print_warning(f"Skipping duplicate theme name={theme.get_name()}")

    # Add the default theme
    #
    if len(_AVAILABLE_THEMES) == 0:
        theme = create_default_theme(computer, folder_path)
    else:
        theme = _AVAILABLE_THEMES[0]

    return theme


def create_default_theme(computer: Computer, theme_path: str = None) -> Theme:
    theme = Theme(computer)
    copy_theme(theme, theme_path + 'Default.cfg')
    theme.save()

    return theme


def get_last_theme() -> tuple[int, None | Theme]:
    max_time = 0
    profile_numb = 0
    theme_name = None

    for num, theme in enumerate(_AVAILABLE_THEMES):

        theme_time = theme.get_time()

        if theme_time > max_time:
            max_time = theme_time
            profile_numb = num
            theme_name = theme.get_name()

    return profile_numb, theme_name


def load_theme_from_file(computer: Computer, path: str) -> Theme:
    print_debug('path="{}"'.format(path))

    with open(path, encoding='utf-8', mode='rt') as f:
        lines = f.readlines()

    area = None
    left_color = ""
    right_color = ""
    mode = ""
    imported_areas = []
    supported_region_names = computer.get_regions_name()
    print_debug(f'supported_region_names={supported_region_names}', direct_output=True)

    theme = Theme(computer)
    theme.path = path

    # Parse the configuration file
    #
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
    global _AVAILABLE_THEMES

    new_theme = Theme(computer=theme._computer)
    new_theme.path = path
    new_theme.set_speed(theme.get_speed())

    for region in theme._computer.get_regions():
        area = Area(region)
        areaitem = AreaItem(mode=theme._computer.default_mode,
                            left_color=_MISSING_ZONE_COLOR,
                            right_color=_MISSING_ZONE_COLOR)

        area.add_item(areaitem)
        theme.add_area(area)

    _AVAILABLE_THEMES.append(theme)

    return new_theme
