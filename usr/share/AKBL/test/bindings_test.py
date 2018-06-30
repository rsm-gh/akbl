#!/usr/bin/python3
#

#  Copyright (C) 2018  Rafael Senties Martinelli 
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


import time
from AKBL.Bindings import Bindings

AKBLConnection = Bindings()


if not AKBLConnection.ping():
    print("The conection with the daemon is off")
else:
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
        print('\tlights off:', AKBLConnection.set_lights(False))
        time.sleep(2)
        print('\tlights on:', AKBLConnection.set_lights(True))
        time.sleep(2)
        print('\tswitch lights:', AKBLConnection.switch_lights())
        time.sleep(2)
        print('\tswitch lights:', AKBLConnection.switch_lights())
        time.sleep(2)

    if profiles_test:
        print("\nTesting user profiles")
        for profile_name in AKBLConnection.get_profile_names():
            print('\tset profile:', profile_name, AKBLConnection.set_profile(profile_name))
            time.sleep(5)

    color1 = '#F7F200'
    color2 = '#ff0000'

    if modes_test:
        print("\nModes test")
        print('\tset_colors fixed', AKBLConnection.set_colors('fixed', 100, color1))            
        time.sleep(5)
        print('\tset_colors blink', AKBLConnection.set_colors('blink', 100, color1))
        time.sleep(5)
        print('\tset_colors morph', AKBLConnection.set_colors('morph', 100, color1, color2))
        time.sleep(5)

    if speed_test:
        print("\nSpeed test on mode blink")
        print('\tset_colors: speed=1', AKBLConnection.set_colors('blink',1,color2))
        time.sleep(5)
        print('\tset_colors: speed=100', AKBLConnection.set_colors('blink',100,color2))
        time.sleep(5)
        print('\tset_colors: speed=255', AKBLConnection.set_colors('blink',255,color2))
        time.sleep(5)


    if colors_multiple_test:
        print("\nMultiple colors test")
        colors1 = ('#FF0000','#FFFF00','#3F33FF') # red, yellow, #blue
        colors2 = ('#FF0000','#FFFF00','#3F33FF')

        print('\tset_colors: multiple fixed', AKBLConnection.set_colors('fixed', 100, colors1))
        time.sleep(15)
        print('\tset_colors: multiple blink', AKBLConnection.set_colors('blink', 100, colors1))
        time.sleep(15)
        print('\tset_colors: multiple morph', AKBLConnection.set_colors('morph', 100, colors1, colors2))
