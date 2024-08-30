#!/usr/bin/python3
#

#  Copyright (C) 2018-2024 Rafael Senties Martinelli.
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
from AKBL.console_printer import print_debug, print_warning, print_error

_SOFTWARE_PATHS = Paths()


def get_all_computers() -> list[Computer]:
    computers = []

    path = Paths()._computers_configuration_dir

    for file_name in os.listdir(path):
        if file_name.endswith(".ini"):

            file_path = os.path.join(path, file_name)

            computer = get_computer_by_path(file_path)

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


def get_compatible_computers() -> list[Computer]:
    driver = Driver()

    compatible_computers = []

    for installed_computer in get_all_computers():
        driver.load_device(installed_computer.vendor_id, installed_computer.product_id)

        if driver.has_device():
            compatible_computers.append(installed_computer)

    return compatible_computers


def get_computer_by_path(file_path: str) -> None | Computer:
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
                region = Region(name=config[section]["ID"],
                                description=config[section]["DESCRIPTION"],
                                hex_id=int(config[section]["BLOCK"]),
                                max_commands=int(config[section]["SUPPORTED_COMMANDS"]),
                                can_blink=config[section]["CAN_BLINK"].lower() == "true",
                                can_morph=config[section]["CAN_MORPH"].lower() == "true",
                                can_light=config[section]["CAN_LIGHT"].lower() == "true")

                computer.add_region(region)

            except Exception:
                print_error("Corrupted region: {} in {}.\n\n".format(section, file_path))
                traceback.print_exc()

    return computer


def get_default_computer() -> None | Computer:
    if not os.path.exists(_SOFTWARE_PATHS._default_computer_file):
        return None

    return get_computer_by_path(_SOFTWARE_PATHS._default_computer_file)


def set_default_computer(computer_name: str):
    computer = None
    for inst_computer in get_all_computers():
        if inst_computer.name == computer_name:
            computer = inst_computer
            break

    if computer is None:
        print_warning("Computer name '{}' not found.".format(computer_name))

    with open(computer.configuration_path, 'r') as f:
        installed_data = f.read()

    with open(_SOFTWARE_PATHS._default_computer_file, 'w') as f:
        f.write(installed_data)
