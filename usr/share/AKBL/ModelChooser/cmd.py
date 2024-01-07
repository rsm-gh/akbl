#!/usr/bin/python3
#

#  Copyright (C) 2024 Rafael Senties Martinelli.
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


import AKBL.Computer.factory as computer_factory

computer = computer_factory.get_installed_computer()

if computer is None:

    compatible_computers = computer_factory.get_compatible_computers()

    if len(compatible_computers) == 0:
        print("Error: No configuration is available for this hardware.")

    elif len(compatible_computers) == 1:
        computer = compatible_computers[0]

    else:
        print("There are multiple configurations that can be used for your computer. Please select the one that matches your computer:")
        for i, comp in enumerate(compatible_computers, 1):
            print("    {}) {}".format(i, comp.name))

        print("\n    or press 0 to quit.\n")

        while True:

            inp = input("Enter the number: ")

            try:
                inp = int(inp)
            except Exception:
                print("    Error, only numbers are accepted.")

            else:
                if inp == 0:
                    break
                else:
                    if inp > len(compatible_computers):
                        print("    Error, the number is not in the list")
                    else:
                        computer = compatible_computers[i-1]
                        break



#
# Re-install the computer configuration
#
if computer is not None:
    print("Installed computer set to: {}".format(computer.name))
    computer_factory.set_installed_computer(computer.name)