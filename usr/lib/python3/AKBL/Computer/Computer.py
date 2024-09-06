#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
#                2011-2012 the pyAlienFX team.
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
import sys

akbl_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if akbl_path not in sys.path:
    sys.path.insert(0, akbl_path)

from Computer.Region import Region
from console_printer import print_warning


class Computer:

    def __init__(self) -> None:

        self.name = 'Undefined'
        self.default_mode = 'fixed'
        self.default_speed = 1
        self.configuration_path = ""
        self.__regions = {}

        self.vendor_id = 6268
        self.product_id = None
        self.supported_commands = 15
        self.data_length = 9
        self.start_byte = 2
        self.fill_byte = 0

        self.state_ready = 16
        self.state_busy = 17
        self.state_unknown_command = 18

        self.command_end_storage = 0
        self.command_set_morph_color = 1
        self.command_set_blink_color = 2
        self.command_set_color = 3

        self.command_loop_block_end = 4
        self.command_transmit_execute = 5
        self.command_get_status = 6
        self.command_reset = 7
        self.command_save_next = 8
        self.command_save = 9
        self.command_battery_state = 15
        self.command_set_speed = 14

        self.reset_touch_controls = 1
        self.reset_sleep_lights_on = 2
        self.reset_all_lights_off = 3
        self.reset_all_lights_on = 4

        self.block_load_on_boot = 1
        self.block_standby = 2
        self.block_ac_power = 5
        self.block_charging = 6

        self.block_battery_sleeping = 7
        self.block_battery_power = 8
        self.block_battery_critical = 9

        self.region_all_but_power = 1023999

    def __str__(self) -> str:
        attributes = '\n'.join(['{}={}'.format(attribute, value) for attribute, value in self.__dict__.items() if
                                not attribute.startswith('_')])
        regions = '\nregions:\n' + '\n'.join([str(region) for region in self.__regions])

        return attributes + regions

    def add_region(self, new_region: Region) -> None:

        if new_region._name in self.__regions:
            print_warning("Duplicated region name={}".format(new_region._name))
            return

        for region in self.__regions.values():
            if region._hex_id == new_region._hex_id:
                print_warning("Duplicated region block={}".format(region._hex_id))
                return

        self.__regions[new_region._name] = new_region

    def get_regions(self) -> list[Region]:
        return list(self.__regions.values())

    def get_regions_name(self) -> list[str]:
        return list(self.__regions.keys())

    def get_region_by_name(self, region_name: str) -> None | Region:
        try:
            return self.__regions[region_name]
        except KeyError:
            return None
