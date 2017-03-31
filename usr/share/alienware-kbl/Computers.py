#!/usr/bin/python3
#

#  Copyright (C) 2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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

from Texts import *
from Region import Region

class Computer:

    def __init__(self):

        self.default_color = '0000FF'
        self.default_mode = 'fixed'
        self.regions = {}

        self.NAME = 'Common Configuration'
        self.VENDOR_ID = 0x187c
        self.PRODUCT_ID = None
        self.SUPPORTED_COMMANDS = 15
        self.DATA_LENGTH = 9
        self.START_BYTE = 0x02
        self.FILL_BYTE = 0x00

        self.STATE_BUSY = 0x11
        self.STATE_READY = 0x10
        self.STATE_UNKNOWN_COMMAND = 0x12

        self.COMMAND_END_STORAGE = 0x00
        self.COMMAND_SET_MORPH_COLOR = 0x01
        self.COMMAND_SET_BLINK_COLOR = 0x02
        self.COMMAND_SET_COLOR = 0x03
        self.COMMAND_LOOP_BLOCK_END = 0x04
        self.COMMAND_TRANSMIT_EXECUTE = 0x05
        self.COMMAND_GET_STATUS = 0x06
        self.COMMAND_RESET = 0x07
        self.COMMAND_SAVE_NEXT = 0x08
        self.COMMAND_SAVE = 0x09
        self.COMMAND_BATTERY_STATE = 0x0F
        self.COMMAND_SET_SPEED = 0x0E

        self.RESET_TOUCH_CONTROLS = 0x01
        self.RESET_SLEEP_LIGHTS_ON = 0x02
        self.RESET_ALL_LIGHTS_OFF = 0x03
        self.RESET_ALL_LIGHTS_ON = 0x04

        self.BLOCK_LOAD_ON_BOOT = 0x01
        self.BLOCK_STANDBY = 0x02
        self.BLOCK_AC_POWER = 0x05
        self.BLOCK_CHARGING = 0x06
        self.BLOCK_BATT_SLEEPING = 0x07
        self.BLOCK_BAT_POWER = 0x08
        self.BLOCK_BATT_CRITICAL = 0x09



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

        self.regions = {

            TEXT_AREA_KEYBOARD_ID : Region(
                TEXT_AREA_KEYBOARD_ID, 
                TEXT_DESCRIPTION_KEYBOARD, 
                self.REGION_KEYBOARD, 
                self.SUPPORTED_COMMANDS, 
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),
                
            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                False, True, False,
                self.default_color)
        }


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

        self.REGION_RIGHT_KEYBOARD = 0x0008
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0004
        self.REGION_LEFT_KEYBOARD = 0x0001
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0002
        self.REGION_RIGHT_SPEAKER = 0x0040
        self.REGION_LEFT_SPEAKER = 0x0020
        self.REGION_ALIENWARE_HEAD = 0x0080
        self.REGION_ALIENWARE_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self.regions = {
            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),
    
            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_EYES_ID : Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True,
                self.default_color)
        }


class Alienware13(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_ALIENWAREWARE13
        self.PRODUCT_ID = 0x0527

        self.REGION_RIGHT_KEYBOARD = 0x0001  # 0x200 seems to work too
        self.REGION_LEFT_KEYBOARD = 0x0008
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x100
        self.REGION_ALIENWARE_NAME = 0x0040
        self.REGION_ALIENWARE_HEAD = 0x0100
        self.REGION_OUTER_LID = 0x0020  # to test the modes morph, blink, etc
        self.REGION_ALL_BUT_POWER = 0x0f9fff  # does this work?
        self.REGION_HARD_DISK_DRIVE = 0x0200
        self.REGION_CAPS_LOCK = 0x80

        self.regions = {
            TEXT_AREA_HARD_DISK_DRIVE_ID : Region(
                TEXT_AREA_HARD_DISK_DRIVE_ID,
                TEXT_DESCRIPTION_HDD,
                self.REGION_HARD_DISK_DRIVE,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_CAPS_LOCK_ID : Region(
                TEXT_AREA_CAPS_LOCK_ID,
                TEXT_DESCRIPTION_CAPS_LOCK,
                self.REGION_CAPS_LOCK,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_OUTER_LID_ID : Region(
                TEXT_AREA_ALIENWARE_OUTER_LID_ID,
                TEXT_DESCRIPTION_OUTER_LID,
                self.REGION_OUTER_LID,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),
        }


class Alienware13R3(Alienware13):

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


class M15XArea51(Computer):

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

        self.regions = {
            TEXT_AREA_LIGHT_PIPE_ID : Region(
                TEXT_AREA_LIGHT_PIPE_ID,
                TEXT_DESCRIPTION_LIGHT_PIPE,
                self.REGION_LIGHTPIPE,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_KEYBOARD_ID : Region(
                TEXT_AREA_KEYBOARD_ID,
                TEXT_DESCRIPTION_KEYBOARD,
                self.REGION_KEY_BOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_LOGO,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_TOUCH_PANEL,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                1,
                False, False, True,
                self.default_color)
        }


class Alienware15(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_ALIENWAREWARE15
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

        self.regions = {
            TEXT_AREA_TACTX_ID : Region(
                TEXT_AREA_TACTX_ID,
                TEXT_DESCRIPTION_TACTX,
                self.REGION_TACTX,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_EYES_ID : Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True,
                self.default_color)
        }


class Alienware15R3(Alienware15):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_ALIENWAREWARE15R3
        self.PRODUCT_ID = 0x0530

class M17X(Computer):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M17X
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


        self.regions = {
            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_EYES_ID : Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True,
                self.default_color)
        }


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


        self.regions = {
            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_EYES_ID : Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True,
                self.default_color)
        }


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


        self.regions = {
            TEXT_AREA_RIGHT_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_KEYBOARD,
                self.REGION_RIGHT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
                self.REGION_RIGHT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_KEYBOARD,
                self.REGION_LEFT_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_CENTER_KEYBOARD_ID : Region(
                TEXT_AREA_LEFT_CENTER_KEYBOARD_ID,
                TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
                self.REGION_LEFT_CENTER_KEYBOARD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_RIGHT_SPEAKER_ID : Region(
                TEXT_AREA_RIGHT_SPEAKER_ID,
                TEXT_DESCRIPTION_RIGHT_SPEAKER,
                self.REGION_RIGHT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_LEFT_SPEAKER_ID : Region(
                TEXT_AREA_LEFT_SPEAKER_ID,
                TEXT_DESCRIPTION_LEFT_SPEAKER,
                self.REGION_LEFT_SPEAKER,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_HEAD_ID : Region(
                TEXT_AREA_ALIENWARE_HEAD_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_HEAD,
                self.REGION_ALIENWARE_HEAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_ALIENWARE_LOGO_ID : Region(
                TEXT_AREA_ALIENWARE_LOGO_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_LOGO,
                self.REGION_ALIENWARE_NAME,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_TOUCH_PAD_ID : Region(
                TEXT_AREA_TOUCH_PAD_ID,
                TEXT_DESCRIPTION_TOUCHPAD,
                self.REGION_TOUCH_PAD,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_MEDIA_BAR_ID : Region(
                TEXT_AREA_MEDIA_BAR_ID,
                TEXT_DESCRIPTION_MEDIA_BAR,
                self.REGION_MEDIA_BAR,
                self.SUPPORTED_COMMANDS,
                True, True, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_EYES_ID : Region(
                TEXT_AREA_POWER_BUTTON_EYES_ID,
                TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES,
                self.REGION_POWER_BUTTON_EYES,
                1,
                False, False, True,
                self.default_color),

            TEXT_AREA_POWER_BUTTON_ID : Region(
                TEXT_AREA_POWER_BUTTON_ID,
                TEXT_DESCRIPTION_POWER_BUTTON,
                self.REGION_POWER_BUTTON,
                2,
                True, True, True,
                self.default_color)
        }


class M18XRX(M18XR2):

    def __init__(self):
        super().__init__()
        self.NAME = TEXT_M18XRX
        self.PRODUCT_ID = 0x0523


COMPUTERS_LIST = {
    TEXT_M11XR1:M11XR1(),
    TEXT_M11XR2:M11XR2(),
    TEXT_M11XR3:M11XR3(),
    TEXT_M11XR25:M11XR25(),
    TEXT_ALIENWAREWARE13:Alienware13(),
    TEXT_ALIENWAREWARE13R3:Alienware13R3(),
    TEXT_M14XR1:M14XR1(),
    TEXT_M14XR2:M14XR2(),
    TEXT_M14XR3:M14XR3(),
    TEXT_M15XAREA51:M15XArea51(),
    TEXT_ALIENWAREWARE15:Alienware15(),
    TEXT_ALIENWAREWARE15R3:Alienware15R3(),
    TEXT_M17X:M17X(),
    TEXT_M17XR2:M17XR2(),
    TEXT_M17XR3:M17XR3(),
    TEXT_M18XR2:M18XR2(),
    TEXT_M18XRX:M18XRX(),
}



if __name__ == '__main__':
    
    for computer_name, computer in COMPUTERS_LIST.items():
        print(computer_name, 'product_id: ', computer.PRODUCT_ID)
        for region_id, region_object in computer.regions.items():
            print('\t{}\t{}'.format(region_id, region_object.description))
        print('\n')
