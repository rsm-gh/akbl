#!/usr/bin/python3
#

#  Copyright (C) 2014-2018  Rafael Senties Martinelli 
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

from AKBL.Configuration.Region import Region
from AKBL.texts import (TEXT_AURORAR4,
                        TEXT_M11XR1,
                        TEXT_M11XR2,
                        TEXT_M11XR3,
                        TEXT_M11XR25,
                        TEXT_M14XR1,
                        TEXT_M14XR2,
                        TEXT_M14XR3,
                        TEXT_M17X,
                        TEXT_M17XR2,
                        TEXT_M17XR3,
                        TEXT_M18XRX,
                        TEXT_M18XR2,
                        TEXT_M15XAREA51,
                        TEXT_ALIENWAREWARE13, 
                        TEXT_ALIENWAREWARE13R3,
                        TEXT_ALIENWAREWARE15,
                        TEXT_ALIENWAREWARE15R3,
                        TEXT_AREA_POWER_BUTTON_ID,
                        TEXT_DESCRIPTION_POWER_BUTTON,
                        TEXT_AREA_POWER_BUTTON_EYES_ID,
                        TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                        TEXT_AREA_MEDIA_BAR_ID,
                        TEXT_DESCRIPTION_MEDIA_BAR,
                        TEXT_AREA_TOUCH_PAD_ID,
                        TEXT_DESCRIPTION_TOUCHPAD,
                        TEXT_AREA_ALIENWARE_LOGO_ID,
                        TEXT_DESCRIPTION_ALIENWAREWARE_LOGO ,
                        TEXT_AREA_ALIENWARE_HEAD_ID,
                        TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                        TEXT_AREA_ALIENWARE_OUTER_LID_ID,
                        TEXT_DESCRIPTION_OUTER_LID,
                        TEXT_AREA_LEFT_SPEAKER_ID,
                        TEXT_DESCRIPTION_LEFT_SPEAKER,
                        TEXT_AREA_RIGHT_SPEAKER_ID,
                        TEXT_DESCRIPTION_RIGHT_SPEAKER,
                        TEXT_AREA_LEFT_KEYBOARD_ID,
                        TEXT_DESCRIPTION_LEFT_KEYBOARD,
                        TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                        TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                        TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                        TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                        TEXT_AREA_RIGHT_KEYBOARD_ID ,
                        TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                        TEXT_AREA_KEYBOARD_ID,
                        TEXT_DESCRIPTION_KEYBOARD,
                        TEXT_AREA_LIGHT_PIPE_ID,
                        TEXT_DESCRIPTION_LIGHT_PIPE,
                        TEXT_AREA_TACTX_ID,
                        TEXT_DESCRIPTION_TACTX,
                        TEXT_AREA_HARD_DISK_DRIVE_ID,
                        TEXT_DESCRIPTION_HDD,
                        TEXT_AREA_CAPS_LOCK_ID,
                        TEXT_DESCRIPTION_CAPS_LOCK)


class Computer(object):

    def __init__(self):

        self.DEFAULT_COLOR = '#0000FF'
        self.DEFAULT_MODE = 'fixed'
        self.DEFAULT_SPEED = 255
        
        self.NAME = 'Common Configuration'
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
        self.COMMAND_SET_MORPH_COLOR = 1
        self.COMMAND_SET_BLINK_COLOR = 2
        self.COMMAND_SET_COLOR = 3
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
        
        self._REGIONS = []
        
    def __str__(self):
        attributes = '\n'.join(['{}={}'.format(attribute, value) for attribute, value in self.__dict__.items() if not attribute.startswith('_')])
        regions = '\nregions:\n'+'\n'.join([str(region) for region in self._REGIONS])
    
        return attributes+regions

    def get_power_block(self):
        return self._power_block
        
    def get_supported_regions_name(self):
        return [region.name for region in self._REGIONS]

    def get_regions(self):
        return self._REGIONS
    
    def get_region_by_name(self, region_name):
        for region in self._REGIONS:
            if region_name == region.name:
                return region

class AuroraR4(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_AURORAR4
        self.PRODUCT_ID = 0x0513

        self.REGION_RIGHT_KEYBOARD = 8
        self.REGION_RIGHT_CENTER_KEYBOARD = 4
        self.REGION_LEFT_KEYBOARD = 1
        self.REGION_LEFT_CENTER_KEYBOARD = 2
        self.REGION_RIGHT_SPEAKER = 64
        self.REGION_LEFT_SPEAKER = 32
        self.REGION_ALIENWARE_HEAD = 128
        self.REGION_ALIENWARE_NAME = 256
        self.REGION_TOUCH_PAD = 512
        self.REGION_MEDIA_BAR = 7168
        self.REGION_POWER_BUTTON = 8192
        self.REGION_POWER_BUTTON_EYES = 16348
        self.REGION_ALL_BUT_POWER = 1023999

        self._REGIONS = [

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),
    
            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class M11XR1(Computer):

    def __init__(self):
        super().__init__()

        self.NAME = TEXT_M11XR1
        self.PRODUCT_ID = 0x0514

        self.REGION_KEYBOARD = 0x0001
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIENWARE_NAME = 0x0100
        self.REGION_MEDIA_BAR = 0x0800
        self.REGION_POWER_BUTTON = 0x6000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self._REGIONS = [

            Region(
                TEXT_AREA_KEYBOARD_ID, 
                TEXT_DESCRIPTION_KEYBOARD, 
                self.REGION_KEYBOARD, 
                self.SUPPORTED_COMMANDS, 
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),
                
            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                False, True, False)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class M11XR2(M11XR1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M11XR2
        self.PRODUCT_ID = 0x0515

class M11XR3(M11XR1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M11XR3
        self.PRODUCT_ID = 0x0522

class M11XR25(M11XR1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M11XR25
        self.PRODUCT_ID = 0x0516

class M14XR1(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M14XR1
        self.PRODUCT_ID = 0x0521

        self.REGION_RIGHT_KEYBOARD = 8
        self.REGION_RIGHT_CENTER_KEYBOARD = 4
        self.REGION_LEFT_KEYBOARD = 1
        self.REGION_LEFT_CENTER_KEYBOARD = 2
        self.REGION_RIGHT_SPEAKER = 64
        self.REGION_LEFT_SPEAKER = 32
        self.REGION_ALIENWARE_HEAD = 128
        self.REGION_ALIENWARE_NAME = 256
        self.REGION_TOUCH_PAD = 512
        self.REGION_MEDIA_BAR = 7168
        self.REGION_POWER_BUTTON = 8192
        self.REGION_POWER_BUTTON_EYES = 16348
        self.REGION_ALL_BUT_POWER = 1023999

        self._REGIONS = [

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),
    
            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class Alienware13R1(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = 'Alienware13R1'
        self.PRODUCT_ID = 0x0527

        # This was updated on Nov 16 2017 with the values given in the following post:
        #       https://github.com/rsm-gh/alienware-kbl/issues/36#issuecomment-344878780
        #
        # The previous values given by Francesco Rosa will be put as comment...
        #

        self.REGION_RIGHT_KEYBOARD = 1  # 512 seems to work too
        self.REGION_LEFT_KEYBOARD = 8
        self.REGION_LEFT_CENTER_KEYBOARD = 4
        self.REGION_RIGHT_CENTER_KEYBOARD = 2 # OLD VALUE=256
        self.REGION_ALIENWARE_NAME = 64
        self.REGION_ALIENWARE_HEAD = 256
        self.REGION_OUTER_LID = 32  # The modes morph & blink haven't been tested here
        self.REGION_ALL_BUT_POWER = 0x0f9fff  # does this work?
        self.REGION_HARD_DISK_DRIVE = 512
        self.REGION_CAPS_LOCK = 128
    
        # 1048476 head, hdd, CapsLock, Left keyboard, Center Left Keyboard


        self._REGIONS = [

            Region(
                TEXT_AREA_HARD_DISK_DRIVE_ID,
                TEXT_DESCRIPTION_HDD,
                self.REGION_HARD_DISK_DRIVE,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_CAPS_LOCK_ID,
                TEXT_DESCRIPTION_CAPS_LOCK,
                self.REGION_CAPS_LOCK,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                "OL",
                TEXT_DESCRIPTION_OUTER_LID,
                self.REGION_OUTER_LID,
                self.SUPPORTED_COMMANDS,
                True, True, True),
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class Alienware13R3(Alienware13R1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_ALIENWAREWARE13R3
        self.PRODUCT_ID = 0x0529


class M14XR2(M14XR1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M14XR2
        
        # The M14XR2 and the M14XR1 have the same PRODUCT_ID.
        # They are differenciated by reading the device information,
        # the R2 has the word 'Gaming'.


class M14XR3(M14XR1):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M14XR3
        self.PRODUCT_ID = 0x0525


class M15XRegion51(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M15XAREA51
        self.PRODUCT_ID = 0x0511

        self.REGION_TOUCH_PAD = 0x000001
        self.REGION_LIGHTPIPE = 0x000020
        self.REGION_ALIENWARE_LOGO = 0x000080
        self.REGION_ALIENWARE_HEAD = 0x000100
        self.REGION_KEY_BOARD = 0x000400
        self.REGION_TOUCH_PANEL = 0x010000
        self.REGION_POWER_BUTTON = 0x008000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self._REGIONS = [

            Region(
                TEXT_AREA_LIGHT_PIPE_ID,
                TEXT_DESCRIPTION_LIGHT_PIPE,
                self.REGION_LIGHTPIPE,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_KEYBOARD_ID,
                TEXT_DESCRIPTION_KEYBOARD,
                self.REGION_KEY_BOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_LOGO,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_TOUCH_PANEL,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                1,
                False, False, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class Alienware15R1(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = "Alienware15R1"
        self.PRODUCT_ID = 0x0528

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x8
        self.REGION_LEFT_CENTER_KEYBOARD = 0x4
        self.REGION_LEFT_SPEAKER = 0x800
        self.REGION_RIGHT_SPEAKER = 0x1000
        self.REGION_POWER_BUTTON = 0x0100
        self.REGION_TOUCH_PAD = 0x400
        self.REGION_ALL_BUT_POWER = 0x7fff
        self.REGION_ALIENWARE_NAME = 0x0040
        self.REGION_ALIENWARE_HEAD = 0x0020
        self.REGION_MEDIA_BAR = 0x0080
        self.REGION_TACTX = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        # 0x1800 primitive speaker-both

        self._REGIONS = [

            Region(
                TEXT_AREA_TACTX_ID,
                TEXT_DESCRIPTION_TACTX,
                self.REGION_TACTX,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class Alienware15R3(Alienware15R1):

    def __init__(self):
        super().__init__()
        self.NAME = "Alienware15R3"
        self.PRODUCT_ID = 0x0530

class M17X(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = "M17XR1"
        self.PRODUCT_ID = 0x0524

        self.REGION_RIGHT_KEYBOARD = 0x0008
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0001
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_SPEAKER = 0x0040
        self.REGION_LEFT_SPEAKER = 0x0020
        self.REGION_ALIENWARE_HEAD = 0x0080
        self.REGION_ALIENWARE_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff


        self._REGIONS = [

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class M17XR2(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M17XR2
        self.PRODUCT_ID = 0x0512

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0004
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0008
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIENWARE_HEAD = 0x0080
        self.REGION_ALIENWARE_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self._REGIONS = [

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class M17XR3(M17X):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M17XR3
        self.PRODUCT_ID = 0x0520


class M18XR2(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M18XR2
        self.PRODUCT_ID = 0x0518

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0008
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIENWARE_HEAD = 0x0080
        self.REGION_ALIENWARE_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self._REGIONS = [

            Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True),

            Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True),

            Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True)
        ]
        
        self._REGIONS.sort(key=lambda region: region.description)


class M18XRX(M18XR2):

    def __init__(self):
        super().__init__()
        self.NAME = 'M18XR1'
        self.PRODUCT_ID = 0x0523


AVAILABLE_COMPUTERS = [ 
    AuroraR4(),
    M11XR1(),
    M11XR2(),
    M11XR3(),
    M11XR25(),
    Alienware13R1(),
    Alienware13R3(),
    M14XR1(),
    M14XR2(),
    M14XR3(),
    M15XRegion51(),
    Alienware15R1(),
    Alienware15R3(),
    M17X(),
    M17XR2(),
    M17XR3(),
    M18XR2(),
    M18XRX(),
]

AVAILABLE_COMPUTERS.sort(key= lambda computer: computer.NAME)


if __name__ == '__main__':
    
    """
    for computer in AVAILABLE_COMPUTERS:
        print(computer.NAME, 'product_id: ', computer.PRODUCT_ID)
        print('\n{}\n'.format(computer.get_supported_regions_name()))
        for region in computer.get_regions():
            print('\t{}\t{}'.format(region.name, region.description))
        print('\n')
    """
    
    from AKBL.Configuration.computer_factory import get_computers
    
    for computer in get_computers():
        
        found=False
        
        for old_computer in AVAILABLE_COMPUTERS:
            
            if old_computer.NAME == computer.NAME:
                found=True
                
                print("CHECKING COMPUTER = {}".format(computer.NAME))
                
                computer_dict = computer.__dict__
                
                for old_key, old_value in old_computer.__dict__.items():
                    
                    if not old_key.startswith("_"):
                        
                        value = computer_dict.get(old_key)
                        
                        if value != old_value:
                            
                            if not old_key.startswith("REGION_") and old_key == "REGION_ALL_BUT_POWER":
                            
                                print("    ERROR ON OLD_KEY={}, {} != {}" .format(old_key, value, old_value))
                                
                                
                for old_region in old_computer.get_regions():
                    
                    new_region = computer.get_region_by_name(old_region.name)
                    
                    if new_region is None:
                        print("    MISSING OLD REGION ID={}".format(old_region.name))
                    else:
                        #print("   Checking region ID={}".format(new_region.name))
                        if old_region.hex_id != new_region.hex_id:
                            print("    region id={}, hex_id error:  {} != {}".format(old_region.name, old_region.hex_id, new_region.hex_id))
                        
            
                        if old_region.max_commands != new_region.max_commands:
                            print("    extra region id={}, max_commands  error:  {} != {}".format(old_region.name, old_region.max_commands , new_region.max_commands ))
                                
                
                                

                for old_region in computer.get_regions():
                    
                    new_region = old_computer.get_region_by_name(old_region.name)
                    
                    if new_region is None:
                        print("    EXTRA REGION ID={}".format(old_region.name))
                    else:
                        #print("   Checking region ID={}".format(new_region.name))
                        if old_region.hex_id != new_region.hex_id:
                            print("    extra region id={}, hex_id error:  {} != {}".format(old_region.name, old_region.hex_id, new_region.hex_id))
                        
                        #if old_region.description != new_region.description:
                        #    print("    extra region id={}, description error:  {} != {}".format(old_region.name, old_region.description, new_region.description))
                        

            
        
        if not found:
            print("MISSING NEW COMPUTER = {}".format(computer.NAME))
                
        
    
    
    