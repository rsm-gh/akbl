#!/usr/bin/python3
#

#  Copyright (C) 2016, 2018, 2024 Rafael Senties Martinelli.
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
import re
import pwd
import subprocess


def get_alienware_device_info():
    cmd = subprocess.run("lsusb", stdout=subprocess.PIPE)
    device_info = cmd.stdout.decode('utf-8', errors="ignore")

    for line in device_info.split("\n"):
        if "alienware" in line.lower():
            bus_id = line.split()[1]
            device_id = line.split()[3][:-1]

            path = "/dev/bus/usb/{}/{}".format(bus_id, device_id)
            cmd = subprocess.run(['lsusb', '-D', path], stdout=subprocess.PIPE)

            device_info += "\n" + cmd.stdout.decode('utf-8', errors="ignore")
            break

    return device_info


def getuser():
    return pwd.getpwuid(os.geteuid()).pw_name


def string_is_hex_color(string):
    if isinstance(string, str) and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', string):
        return True

    return False


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))
