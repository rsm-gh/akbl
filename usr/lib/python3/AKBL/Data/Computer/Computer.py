#!/usr/bin/python3
#

#  Copyright (C) 2014-2018  RSM
#                2011-2012  the pyAlienFX team
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
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.

from AKBL.utils import print_warning

class Computer(object):

    def __init__(self):
        
        self.DEFAULT_MODE = 'fixed'
        
        self.NAME = 'Default Configuration'
        self.VENDOR_ID = 6268
        self.PRODUCT_ID = None
        self.SUPPORTED_COMMANDS = 15
        self.DATA_LENGTH = 9
        self.START_BYTE = 2
        self.FILL_BYTE = 0

        self.STATE_BUSY = 17
        self.STATE_READY = 16
        self.STATE_UNKNOWN_COMMAND = 18

        self.COMMAND_END_STORAGE = 0
        self.COMMAND_SET_COLOR = 3
        self.COMMAND_SET_MORPH_COLOR = 1
        self.COMMAND_SET_BLINK_COLOR = 2
        self.COMMAND_LOOP_BLOCK_END = 4
        self.COMMAND_TRANSMIT_EXECUTE = 5
        self.COMMAND_GET_STATUS = 6
        self.COMMAND_RESET = 7
        self.COMMAND_SAVE_NEXT = 8
        self.COMMAND_SAVE = 9
        self.COMMAND_BATTERY_STATE = 15
        self.COMMAND_SET_SPEED = 14

        self.RESET_TOUCH_CONTROLS = 1
        self.RESET_SLEEP_LIGHTS_ON = 2
        self.RESET_ALL_LIGHTS_OFF = 3
        self.RESET_ALL_LIGHTS_ON = 4

        self.BLOCK_LOAD_ON_BOOT = 1
        self.BLOCK_STANDBY = 2
        self.BLOCK_AC_POWER = 5
        self.BLOCK_CHARGING = 6
        self.BLOCK_BATT_SLEEPING = 7
        self.BLOCK_BAT_POWER = 8
        self.BLOCK_BATT_CRITICAL = 9
        
        self.REGION_ALL_BUT_POWER = 1023999
        
        self.__regions = []
        self.__regions.sort(key=lambda region: region.description)
        
        
    def __str__(self):
        attributes = '\n'.join(['{}={}'.format(attribute, value) for attribute, value in self.__dict__.items() if not attribute.startswith('_')])
        regions = '\nregions:\n'+'\n'.join([str(region) for region in self.__regions])
    
        return attributes+regions
        
    def get_regions(self):
        return self.__regions
        
    def get_regions_name(self):
        return [region.name for region in self.__regions]
    
    def get_region_by_name(self, region_name):
        for region in self.__regions:
            if region_name == region.name:
                return region
            
        return None

    def add_region(self, new_region):
        
        for region in self.__regions:
                        
            if region.name == new_region.name:
                print_warning("Duplicated region id={}".format(region.name))
                return
            
            elif region.hex_id == new_region.hex_id:
                print_warning("Duplicated region block={}".format(region.hex_id))
                return
            
        self.__regions.append(new_region)
