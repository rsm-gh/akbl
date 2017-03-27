#!/usr/bin/python3
#

#  Copyright (C)  2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
#                 2011-2012  the pyAlienFX team
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


TEXT_ADD = "Add"

TEXT_CHOOSE_A_FOLDER_TO_EXPORT = "Choose a folder to export the theme"
TEXT_CHOOSE_A_THEME = "Choose an alienware-kbl theme"
TEXT_THEME_ALREADY_EXISTS = '''There's already a theme with this filename,
do you want to overwrite it?'''


TEXT_COPY_CONFIG = '''It seems that there was an existing alienware-kbl
configuration, probably made by an older version.

Do you want to import it for this user? (yes)
'''

TEXT_PROFILES = "Profiles"
TEXT_START_THE_GUI = "Start the GUI"
TEXT_SWICH_STATE = "Switch State"
TEXT_EXIT = "Exit"

DATA_INFO = '''
 No Alienware device was detected.
'''

DATA_INFO_ERROR = '''
 An error ocurred while retriving the information of your computer. Please
 send this report to rafael@senties-martinelli.com\n
'''

TEXT_HELP = '''
 Usage:
    alienware-kbl <option>

 Options:

    --change                        Changes the state on/off.
    --on                            Turns on the alienware keyboard lights.
    --off                           Turns off the alienware keyboard lights.
    --set-profile <profile name>    Activate a profile

    --get-boot-user                 Get the user that is started by the daemon
    --set-boot-user <username>      Set the user that is started by the daemon

    --start-indicator               Start the indicator.

    -h, -help                       Display this dialog.
    -l, --license                   Display the license.
    -v, --version                   Display the current version.


 *If no option is introduced the graphical interface is launched.

'''

TEXT_LICENSE = '''
  Copyright (C) 2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
                2011-2012  the pyAlienFX team

  This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License 3 as published by
   the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.
 '''

TEXT_ERROR_DAEMON_OFF = "The daemon is off or the connection couldn't be stablished."

TEXT_WRONG_ARGUMENT = '''alienware-kbl: wrong argument. use "alienware-kbl --help"'''

TEXT_VERSION = "alienware-kbl DEB_BUILDER_VERSION"

TEXT_RESTART_THE_SYSTEM = "{0} You will have to restart the system to make it effective."

TEXT_ONLY_FROM_TERMINAL = "** The root permission has been removed. Unfortunately,\nthe launcher will still asking for it. call it from the terminal to skip it. **\n\n"

TEXT_APPLYING_CONFIGURATION = "Applying the configuration.."

TEXT_SHUTTING_LIGHTS_OFF = "Shutting the lights off.."

TEXT_TURNING_LIGHTS_ON = "Turning the lights on.."

TEXT_THE_GUI_NEEDS_ROOT = "The graphical interface needs to be run as root."

TEXT_SAVING_THE_CONFIGURATION = "Saving the configuration.."

TEXT_CONFIGURATION_DELETED = "The configuration has been deleted.."

TEXT_CONFIRM_DELETE_CONFIGURATION = "Are you sure that you want to\n delete this configuration?"

TEXT_COMPUTER_DATA = '''
 Dected As: {0}
 Vendor ID: {1}
 Product ID: {2}

{3}

'''

TEXT_ONLY_ROOT = "This command can only be used by the root user."

TEXT_NON_LINUX_USER = '''The user you wanted to add is not recognized by the system,
it won't be added.'''

TEXT_COMPUTER_NOT_FOUND = "Error: Computer Not Supported"


#
#   Block Testing
#
TEXT_VALUE_CHANGED = '''[Value Changed]: {}\t int: {}\t hex: {}\n'''
TEXT_NON_INTEGER = '''[Error Fixed]: Non integer {}\tvalue:{} .\n'''
TEXT_DEVICE_NOT_FOUND = '''[Device not found]: Vendor ID: {}\t Product ID: {}\n'''
TEXT_DEVICE_FOUND = '''[Device found]: Vendor ID: {}\t Product ID: {}\n'''
TEXT_BLOCK_TEST = '''[TEST]: block: {}\t hex: {}\t mode:{}\t speed:{}\t color1:{}\t color2: {}\n'''
TEXT_BLOCK_LIGHTS_OFF = '''[Command]: Lights off'''

#
#   Zones Description
#

TEXT_DESCRIPTION_POWER_BUTTON = "Power Button"
TEXT_DESCRIPTION_ALIENWARE_POWERBUTTON_EYES = "Power Button: Eyes"
TEXT_DESCRIPTION_MEDIA_BAR = "Media Bar"
TEXT_DESCRIPTION_TOUCHPAD = "Touchpad"
TEXT_DESCRIPTION_ALIENWARE_LOGO = "Logo"
TEXT_DESCRIPTION_ALIENWARE_HEAD = "Head"
TEXT_DESCRIPTION_LEFT_SPEAKER = "Speaker: Left"
TEXT_DESCRIPTION_RIGHT_SPEAKER = "Speaker: Right"
TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD = "Keyboard: Left-Center"
TEXT_DESCRIPTION_LEFT_KEYBOARD = "Keyboard: Left "
TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD = "Keyboard: Righ-Center"
TEXT_DESCRIPTION_RIGHT_KEYBOARD = "Keyboard: Right"
TEXT_DESCRIPTION_KEYBOARD = "Keyboard"
TEXT_DESCRIPTION_TACTX = "Tact-X"
TEXT_DESCRIPTION_OUTER_LID = "Outer Lid"
TEXT_DESCRIPTION_LIGHT_PIPE = "Pipe: Left"
TEXT_DESCRIPTION_ON_BATTERY = "On Battery"
TEXT_DESCRIPTION_CHARGING = "Charging"
TEXT_DESCRIPTION_AC_POWER = "AC Power"
TEXT_DESCRIPTION_STAND_BY = "StandBy"
TEXT_DESCRIPTION_HDD = "Hard Disk Drive"
TEXT_DESCRIPTION_WIFI = "Wifi"
TEXT_DESCRIPTION_CAPS_LOCK = "Caps Lock"
TEXT_DESCRIPTION_BOOT = "Boot"

#
#	Computer Names
#
TEXT_M11XR1 = 'M11XR1'
TEXT_M11XR2 = 'M11XR2'
TEXT_M11XR3 = 'M11XR3'
TEXT_M11XR25 = 'M11XR25'
TEXT_ALIENWARE13 = 'Alienware 13'
TEXT_ALIENWARE13R3 = 'Alienware 13R3'
TEXT_M14XR1 = 'M14XR1'
TEXT_M14XR2 = 'M14XR2'
TEXT_M14XR3 = 'M14XR3'
TEXT_M15XAREA51 = 'M15XArea51'
TEXT_ALIENWARE15 = 'Alienware 15'
TEXT_ALIENWARE15R3 = 'Alienware 15R3'
TEXT_M17X = 'M17X'
TEXT_M17XR2 = 'M17XR2'
TEXT_M17XR3 = 'M17XR3'
TEXT_M18XRX = 'M18XRX'
TEXT_M18XR2 = 'M18XR2'
