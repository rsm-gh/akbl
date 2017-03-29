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
from Area import AreaIDS

class PowerMode:

    def __init__(self, name, description, block):
        self.description = description
        self.name = name

class Region:

    def __init__(
            self,
            name,
            description,
            regionId,
            maxCommands,
            canBlink,
            canMorph,
            canLight,
            default_color,
            default_mode='fixed',
            power_button=False):

        self.name = name
        self.description = description
        self.regionId = regionId
        self.canLight = canLight
        self.canBlink = canBlink
        self.canMorph = canMorph
        self.color1 = default_color
        self.color2 = default_color
        self.mode = default_mode
        self.power_button = power_button
        self.maxCommands = maxCommands
        self.line = {1: Configuration(self.mode, self.color1, self.color2)}

    def update_line(self, Id, mode=None, color1=None, color2=None):
        if Id in self.line:
            if mode:
                self.line[Id].mode = mode
            if color1:
                self.line[Id].color1 = color1
            if color2:
                self.line[Id].color2 = color2
            return True
        return False

    def add_line(self, Id, mode, color1, color2):
        Id = max(self.line.keys())
        if Id + 1 not in self.line:
            self.line[Id + 1] = Configuration(mode, color1, color2)
            return True
        return False


class Configuration:

    def __init__(self, mode, color1, color2=None):
        self.mode = mode
        self.color1 = color1
        self.color2 = color2

    def __str__(self):
        return 'Mode: {0}\t Color1: {1}\t Color2: {2}'.format(
            self.mode, self.color1, self.color2)


class CommonConf:

    def __init__(self):

        self.AreaIDS = AreaIDS()
        self.regions = {}
        self.default_color = '0000FF'
        self.default_mode = 'fixed'

        self.STATE_BUSY = 0x11
        self.STATE_READY = 0x10
        self.STATE_UNKNOWN_COMMAND = 0x12

        self.SUPPORTED_COMMANDS = 15
        self.COMMAND_END_STORAGE = 0x00  # End Storage block (See storage)
        # Set morph color (See set commands)
        self.COMMAND_SET_MORPH_COLOR = 0x01
        # Set blink color (See set commands)
        self.COMMAND_SET_BLINK_COLOR = 0x02
        self.COMMAND_SET_COLOR = 0x03  # Set color (See set commands)
        self.COMMAND_LOOP_BLOCK_END = 0x04  # Loop Block end (See loops)
        self.COMMAND_TRANSMIT_EXECUTE = 0x05  # End transmition and execute
        # Get device status (see get device status)
        self.COMMAND_GET_STATUS = 0x06
        self.COMMAND_RESET = 0x07  # Reset (See reset)
        # Save next instruction in storage block (see storage)
        self.COMMAND_SAVE_NEXT = 0x08
        self.COMMAND_SAVE = 0x09  # Save storage data (See storage)
        # Set batery state (See set commands)
        self.COMMAND_BATTERY_STATE = 0x0F
        self.COMMAND_SET_SPEED = 0x0E  # Set display speed (see set speed)

        self.RESET_TOUCH_CONTROLS = 0x01
        self.RESET_SLEEP_LIGHTS_ON = 0x02
        self.RESET_ALL_LIGHTS_OFF = 0x03
        self.RESET_ALL_LIGHTS_ON = 0x04

        self.DATA_LENGTH = 9

        self.START_BYTE = 0x02
        self.FILL_BYTE = 0x00

        self.BLOCK_LOAD_ON_BOOT = 0x01
        self.BLOCK_STANDBY = 0x02
        self.BLOCK_AC_POWER = 0x05
        self.BLOCK_CHARGING = 0x06
        self.BLOCK_BATT_SLEEPING = 0x07
        self.BLOCK_BAT_POWER = 0x08
        self.BLOCK_BATT_CRITICAL = 0x09


class M11XR1(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M11XR1

        self.REGION_KEYBOARD = 0x0001
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIEN_NAME = 0x0100
        self.REGION_MEDIA_BAR = 0x0800
        self.REGION_POWER_BUTTON = 0x6000
        self.REGION_ALL_BUT_POWER = 0x0f9fff


        self.regions[self.AreaIDS.KEYBOARD_ID] = Region(
            self.AreaIDS.KEYBOARD_ID,
            TEXT_DESCRIPTION_KEYBOARD,
            self.REGION_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            False,
            True,
            False,
            self.default_color,
            self.suportedMode,
            power_button=True)


class M11XR2(M11XR1):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M11XR2


class M11XR3(M11XR1):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M11XR3


class M11XR25(M11XR1):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M11XR25


class M14XR1(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M14XR1

        self.REGION_RIGHT_KEYBOARD = 0x0008
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0004
        self.REGION_LEFT_KEYBOARD = 0x0001
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0002
        self.REGION_RIGHT_SPEAKER = 0x0040
        self.REGION_LEFT_SPEAKER = 0x0020
        self.REGION_ALIEN_HEAD = 0x0080
        self.REGION_ALIEN_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff



        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_EYES_ID] = Region(
            self.AreaIDS.POWER_BUTTON_EYES_ID,
            TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES,
            self.REGION_POWER_BUTTON_EYES,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class Alienware13(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_ALIENWARE13

        self.REGION_RIGHT_KEYBOARD = 0x0001  # 0x200 seems to work too
        self.REGION_LEFT_KEYBOARD = 0x0008
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x100
        self.REGION_ALIEN_NAME = 0x0040
        self.REGION_ALIEN_HEAD = 0x0100
        self.REGION_OUTER_LID = 0x0020  # to test the modes morph, blink, etc
        self.REGION_ALL_BUT_POWER = 0x0f9fff  # does this work?
        self.REGION_HARD_DISK_DRIVE = 0x0200
        self.REGION_CAPS_LOCK = 0x80


        self.regions[
            self.AreaIDS.HARD_DISK_DRIVE_ID] = Region(
            self.AreaIDS.HARD_DISK_DRIVE_ID,
            TEXT_DESCRIPTION_HDD,
            self.REGION_HARD_DISK_DRIVE,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.CAPS_LOCK_ID] = Region(
            self.AreaIDS.CAPS_LOCK_ID,
            TEXT_DESCRIPTION_CAPS_LOCK,
            self.REGION_CAPS_LOCK,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_OUTER_LID_ID] = Region(
            self.AreaIDS.ALIEN_OUTER_LID_ID,
            TEXT_DESCRIPTION_OUTER_LID,
            self.REGION_OUTER_LID,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)


class Alienware13R3(Alienware13):

    def __init__(self):
        super().__init__()
        self.name = TEXT_ALIENWARE13R3


class M14XR2(M14XR1):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M14XR2


class M14XR3(M14XR1):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M14XR3


class M15XArea51(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M15XAREA51

        self.REGION_TOUCH_PAD = 0x000001
        self.REGION_LIGHTPIPE = 0x000020
        self.REGION_ALIEN_LOGO = 0x000080
        self.REGION_ALIEN_HEAD = 0x000100
        self.REGION_KEY_BOARD = 0x000400
        self.REGION_TOUCH_PANEL = 0x010000
        self.REGION_POWER_BUTTON = 0x008000
        self.REGION_ALL_BUT_POWER = 0x0f9fff

        self.regions[
            self.AreaIDS.LIGHT_PIPE_ID] = Region(
            self.AreaIDS.LIGHT_PIPE_ID,
            TEXT_DESCRIPTION_LIGHT_PIPE,
            self.REGION_LIGHTPIPE,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.KEYBOARD_ID] = Region(
            self.AreaIDS.KEYBOARD_ID,
            TEXT_DESCRIPTION_KEYBOARD,
            self.REGION_KEY_BOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_LOGO,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_TOUCH_PANEL,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class Alienware15(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_ALIENWARE15

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x8
        self.REGION_LEFT_CENTER_KEYBOARD = 0x4
        self.REGION_LEFT_SPEAKER = 0x800
        self.REGION_RIGHT_SPEAKER = 0x1000
        self.REGION_POWER_BUTTON = 0x0100
        self.REGION_TOUCH_PAD = 0x400
        self.REGION_ALL_BUT_POWER = 0x7fff
        self.REGION_ALIEN_NAME = 0x0040
        self.REGION_ALIEN_HEAD = 0x0020
        self.REGION_MEDIA_BAR = 0x0080
        self.REGION_TACTX = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        # 0x1800 primitive speaker-both

        self.regions[
            self.AreaIDS.TACTX_ID] = Region(
            self.AreaIDS.TACTX_ID,
            TEXT_DESCRIPTION_TACTX,
            self.REGION_TACTX,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_EYES_ID] = Region(
            self.AreaIDS.POWER_BUTTON_EYES_ID,
            TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES,
            self.REGION_POWER_BUTTON_EYES,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class Alienware15R3(Alienware15):

    def __init__(self):
        super().__init__()
        self.name = TEXT_ALIENWARE15R3


class M17X(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M17X

        self.REGION_RIGHT_KEYBOARD = 0x0008
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0001
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_SPEAKER = 0x0040
        self.REGION_LEFT_SPEAKER = 0x0020
        self.REGION_ALIEN_HEAD = 0x0080
        self.REGION_ALIEN_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff


        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_EYES_ID] = Region(
            self.AreaIDS.POWER_BUTTON_EYES_ID,
            TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES,
            self.REGION_POWER_BUTTON_EYES,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class M17XR2(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M17XR2

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0004
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0008
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIEN_HEAD = 0x0080
        self.REGION_ALIEN_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff


        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_EYES_ID] = Region(
            self.AreaIDS.POWER_BUTTON_EYES_ID,
            TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES,
            self.REGION_POWER_BUTTON_EYES,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class M17XR3(M17X):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M17XR3


class M18XR2(CommonConf):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M18XR2

        self.REGION_RIGHT_KEYBOARD = 0x0001
        self.REGION_RIGHT_CENTER_KEYBOARD = 0x0002
        self.REGION_LEFT_KEYBOARD = 0x0008
        self.REGION_LEFT_CENTER_KEYBOARD = 0x0004
        self.REGION_RIGHT_SPEAKER = 0x0020
        self.REGION_LEFT_SPEAKER = 0x0040
        self.REGION_ALIEN_HEAD = 0x0080
        self.REGION_ALIEN_NAME = 0x0100
        self.REGION_TOUCH_PAD = 0x0200
        self.REGION_MEDIA_BAR = 0x1c00
        self.REGION_POWER_BUTTON = 0x2000
        self.REGION_POWER_BUTTON_EYES = 0x4000
        self.REGION_ALL_BUT_POWER = 0x0f9fff


        self.regions[
            self.AreaIDS.RIGHT_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_KEYBOARD,
            self.REGION_RIGHT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.RIGHT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD,
            self.REGION_RIGHT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_KEYBOARD,
            self.REGION_LEFT_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID] = Region(
            self.AreaIDS.LEFT_CENTER_KEYBOARD_ID,
            TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD,
            self.REGION_LEFT_CENTER_KEYBOARD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.RIGHT_SPEAKER_ID] = Region(
            self.AreaIDS.RIGHT_SPEAKER_ID,
            TEXT_DESCRIPTION_RIGHT_SPEAKER,
            self.REGION_RIGHT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.LEFT_SPEAKER_ID] = Region(
            self.AreaIDS.LEFT_SPEAKER_ID,
            TEXT_DESCRIPTION_LEFT_SPEAKER,
            self.REGION_LEFT_SPEAKER,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_HEAD_ID] = Region(
            self.AreaIDS.ALIEN_HEAD_ID,
            TEXT_DESCRIPTION_ALIENWARE_HEAD,
            self.REGION_ALIEN_HEAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.ALIEN_LOGO_ID] = Region(
            self.AreaIDS.ALIEN_LOGO_ID,
            TEXT_DESCRIPTION_ALIENWARE_LOGO,
            self.REGION_ALIEN_NAME,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.TOUCH_PAD_ID] = Region(
            self.AreaIDS.TOUCH_PAD_ID,
            TEXT_DESCRIPTION_TOUCHPAD,
            self.REGION_TOUCH_PAD,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.MEDIA_BAR_ID] = Region(
            self.AreaIDS.MEDIA_BAR_ID,
            TEXT_DESCRIPTION_MEDIA_BAR,
            self.REGION_MEDIA_BAR,
            self.SUPPORTED_COMMANDS,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_EYES_ID] = Region(
            self.AreaIDS.POWER_BUTTON_EYES_ID,
            TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES,
            self.REGION_POWER_BUTTON_EYES,
            1,
            False,
            False,
            True,
            self.default_color,
            self.suportedMode)
        self.regions[
            self.AreaIDS.POWER_BUTTON_ID] = Region(
            self.AreaIDS.POWER_BUTTON_ID,
            TEXT_DESCRIPTION_POWER_BUTTON,
            self.REGION_POWER_BUTTON,
            2,
            True,
            True,
            True,
            self.default_color,
            self.suportedMode,
            power_button=True)


class M18XRX(M18XR2):

    def __init__(self):
        super().__init__()
        self.name = TEXT_M18XRX


class Computer:

    def __init__(self, name, vendorId, productId, computer):
        self.name = name
        self.vendorId = vendorId
        self.productId = productId
        self.computer = computer


class AllComputers():

    # Define General Device controls
    #
    ALIENFX_USER_CONTROLS = 0x01
    ALIENFX_SLEEP_LIGHTS = 0x02
    ALIENFX_ALL_OFF = 0x03
    ALIENFX_ALL_ON = 0x04

    ALIENFX_MORPH = 0x01
    ALIENFX_BLINK = 0x02
    ALIENFX_STAY = 0x03
    ALIENFX_BATTERY_STATE = 0x0F

    ALIENFX_TOUCHPAD = 0x000001
    ALIENFX_LIGHTPIPE = 0x000020
    ALIENFX_ALIENWARE_LOGO = 0x000080
    ALIENFX_ALIENHEAD = 0x000100
    ALIENFX_POWER_BUTTON = 0x008000
    ALIENFX_TOUCH_PANEL = 0x010000

    ALIENFX_DEVICE_RESET = 0x06
    ALIENFX_READY = 0x10
    ALIENFX_BUSY = 0x11
    ALIENFX_UNKOWN_COMMAND = 0x12

    #
    # If you add a new computer please send me an email/open a bug repport so I can add it to the main program too.
    # The names are taken from wikipedia:  https://en.wikipedia.org/wiki/Alienware
    #
    computerList = {
        # id vendor, id product
        TEXT_M11XR1: Computer(TEXT_M11XR1, 0x187c, 0x0514, M11XR1()),
        TEXT_M11XR2: Computer(TEXT_M11XR2, 0x187c, 0x0515, M11XR2()),
        TEXT_M11XR3: Computer(TEXT_M11XR3, 0x187c, 0x0522, M11XR3()),
        TEXT_M11XR25: Computer(TEXT_M11XR25, 0x187c, 0x0516, M11XR25()),
        TEXT_ALIENWARE13: Computer(TEXT_ALIENWARE13, 0x187c, 0x0527, Alienware13()),
        TEXT_ALIENWARE13R3: Computer(TEXT_ALIENWARE13R3, 0x187c, 0x0529, Alienware13R3()),

        # M14XR2 is differenciated from M14XR1 by reading
        TEXT_M14XR1: Computer(TEXT_M14XR1, 0x187c, 0x0521, M14XR1()),
        # the device information. > Gaming' take a look to Engine.py
        TEXT_M14XR2: Computer(TEXT_M14XR2, 0x187c, 0x0521, M14XR2()),
        TEXT_M14XR3: Computer(TEXT_M14XR3, 0x187c, 0x0525, M14XR3()),

        TEXT_M15XAREA51: Computer(TEXT_M15XAREA51, 0x187c, 0x0511, M15XArea51()),
        TEXT_ALIENWARE15: Computer(TEXT_ALIENWARE15, 0x187c, 0x0528, Alienware15()),
        TEXT_ALIENWARE15R3: Computer(TEXT_ALIENWARE15R3, 0x187c, 0x0530, Alienware15R3()),

        TEXT_M17X: Computer(TEXT_M17X, 0x187c, 0x0524, M17X()),
        TEXT_M17XR2: Computer(TEXT_M17XR2, 0x187c, 0x0512, M17XR2()),
        TEXT_M17XR3: Computer(TEXT_M17XR3, 0x187c, 0x0520, M17XR3()),

        TEXT_M18XRX: Computer(TEXT_M18XRX, 0x187c, 0x0523, M18XRX()),
        TEXT_M18XR2: Computer(TEXT_M18XR2, 0x187c, 0x0518, M18XR2()),
    }
