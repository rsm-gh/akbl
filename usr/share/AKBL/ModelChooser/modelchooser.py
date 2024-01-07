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

import os
import sys

from AKBL.Engine.Driver import Driver
import AKBL.Computer.factory as computer_factory

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

from ModelChooser.ModelChooser import main

driver = Driver()
compatible_computers = []

for computer in computer_factory.get_computers():
    driver.load_device(computer.vendor_id, computer.product_id)
    if driver.has_device():
        compatible_computers.append(computer)


if len(compatible_computers) == 0:
    print("Error: No computer is available with this")

elif len(compatible_computers) == 1:
    print("ONLY ONE COMPUTER")

else:
    print("MULTIPLE COMPUTERS")
    main()
