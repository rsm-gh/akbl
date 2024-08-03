#!/usr/bin/python3
#

#  Copyright (C) 2018-2019, 2024 Rafael Senties Martinelli.
#
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
import traceback
from configparser import ConfigParser

from AKBL.Paths import Paths
from AKBL.Engine.Driver import Driver
from AKBL.Computer.Region import Region
from AKBL.Computer.Computer import Computer
from AKBL.console import print_debug, print_warning, print_error

_SOFTWARE_PATHS = Paths()

def get_compatible_computers():

    driver = Driver()

    compatible_computers = []

    for installed_computer in get_installed_computers():
        driver.load_device(installed_computer.vendor_id, installed_computer.product_id)

        if driver.has_device():
            compatible_computers.append(installed_computer)

    return compatible_computers


def get_installed_computer_by_path(file_path):
    print_debug("Reading {}".format(file_path))

    computer = Computer()
    computer.configuration_path = file_path

    config = ConfigParser()
    config.optionxform = str

    try:
        config.read(file_path)
    except Exception:
        print_error("Corrupted file: {}\n\n{}".format(file_path, traceback.format_exc()))
        return None

    for key in config["COMMON"]:

        lower_key = key.lower()

        if not hasattr(computer, lower_key):
            print_warning("Skipping attribute '{}'".format(key))
            continue

        value = config["COMMON"][key]
        if value == "":
            print_warning("Empty value on attribute '{}'".format(key))
            continue

        if key in ("NAME", "DEFAULT_MODE"):
            setattr(computer, lower_key, value)
        else:
            setattr(computer, lower_key, int(value))

    for section in config.sections():
        if section.startswith("REGION"):

            try:
                region = Region(config[section]["ID"],
                                config[section]["DESCRIPTION"],
                                int(config[section]["BLOCK"]),
                                int(config[section]["SUPPORTED_COMMANDS"]),
                                config[section]["CAN_BLINK"] == "True",
                                config[section]["CAN_MORPH"] == "True",
                                config[section]["CAN_LIGHT"] == "True")

                computer.add_region(region)

            except Exception:
                print_error("Corrupted region: {} in {}.\n\n".format(section, file_path))
                traceback.print_exc()

    return computer


def get_installed_computers():
    computers = []

    path = Paths()._computers_configuration_dir

    for file_name in os.listdir(path):
        if file_name.endswith(".ini"):

            file_path = os.path.join(path, file_name)

            computer = get_installed_computer_by_path(file_path)

            if computer is None:
                continue

            add = True
            for added_computer in computers:
                if computer.name == added_computer:
                    print_warning("Computer name already exists={}".format(computer.name))
                    add = False
                    break

            if add:
                computers.append(computer)

    computers.sort(key=lambda cmp: cmp.name)

    return computers


def get_installed_computer():

    if not os.path.exists(_SOFTWARE_PATHS._default_computer_file):
        return None

    return get_installed_computer_by_path(_SOFTWARE_PATHS._default_computer_file)


def set_installed_computer(computer_name):

    computer = None
    for inst_computer in get_installed_computers():
        if inst_computer.name == computer_name:
            computer = inst_computer
            break

    if computer is None:
        print_warning("Computer name '{}' not found.".format(computer_name))
        return False

    with open(computer.configuration_path, 'r') as f:
        installed_data = f.read()

    with open(_SOFTWARE_PATHS._default_computer_file, 'w') as f:
        f.write(installed_data)

    return True

def get_installed_computer_by_name(name):
    for computer in get_installed_computers():
        if computer.name == name:
            return computer

    return None
