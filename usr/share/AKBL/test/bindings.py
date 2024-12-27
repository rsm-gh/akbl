#!/usr/bin/python3
#

#  Copyright (C) 2018-2024 Rafael Senties Martinelli.
#
#  AKBL is free software; you can redistribute it and/or modify
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


import time
from AKBL.Bindings import Bindings

akbl = Bindings()

if not akbl.ping():
    print("The connection with the daemon is off")
    exit()

"""
    Each command is called as:

        print( <command_name>, <command> )

    To check if the commands succeed. You don't
    really need to do this in your code!
"""

lights_test = True
profiles_test = True
modes_test = True
speed_test = True
colors_multiple_test = True

if lights_test:
    print("Switching lights test")
    print('\tlights off:', akbl.set_lights(False))
    time.sleep(2)
    print('\tlights on:', akbl.set_lights(True))
    time.sleep(2)
    print('\tswitch lights:', akbl.switch_lights())
    time.sleep(2)
    print('\tswitch lights:', akbl.switch_lights())
    time.sleep(2)

if profiles_test:
    print("\nTesting user profiles")
    for theme_name in akbl.get_themes_name():
        print('\tset profile:', theme_name, akbl.set_theme(theme_name))
        time.sleep(5)

single_colors = ['#F7F200']
morph_colors = [('#F7F200', '#ff0000')]

if modes_test:
    print("\nModes test")
    print('\tset_colors fixed', akbl.set_fixed_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors blink', akbl.set_blink_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors morph', akbl.set_morph_mode(morph_colors, 100))
    time.sleep(5)

if speed_test:
    print("\nSpeed test on mode blink")
    print('\tset_colors: speed=1', akbl.set_blink_mode(single_colors, 1))
    time.sleep(5)
    print('\tset_colors: speed=100', akbl.set_blink_mode(single_colors, 100))
    time.sleep(5)
    print('\tset_colors: speed=255', akbl.set_blink_mode(single_colors, 255))
    time.sleep(5)

if colors_multiple_test:
    print("\nMultiple colors test")
    single_colors = ['#FF0000', '#FFFF00', '#3F33FF']  # red, yellow, #blue
    morph_colors = [('#FF0000', '#3F33FF'),
                    ('#FFFF00', '#3F33FF'),
                    ('#FF0000', '#3F33FF')]

    print('\tset_colors: multiple fixed', akbl.set_fixed_mode(single_colors, 100))
    time.sleep(15)
    print('\tset_colors: multiple blink', akbl.set_blink_mode(single_colors, 100))
    time.sleep(15)
    print('\tset_colors: multiple morph', akbl.set_morph_mode(morph_colors, 100))
