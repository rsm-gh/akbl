#!/usr/bin/python3
#

#  Copyright (C)  2014-2017  Rafael Senties Martinelli 
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
 send this report to https://github.com/rsm-gh/alienware-kbl/issues\n
'''

TEXT_HELP = '''
Usage:

    alienware-kbl <option>

 Options:

    --change                          Changes the computer lights on/off.
    --on                              Turns on the computer lights.
    --off                             Turns off the computer lights.
    --set-profile <profile_name>      Turns on the selected profile.
    
    --start-indicator                 Start the indicator.
    
    --start-daemon                    Start the daemon.
    --daemon-is-on                    Returns weather the daemon is running or not.
    
    --block-testing                   Display the block testing window.
    
    -h, -help                         Display this dialog.
    -l, --license                     Display the license.

 *If no option is introduced the graphical interface is launched.
'''

TEXT_LICENSE = '''
  Copyright (C) 2014-2017  Rafael Senties Martinelli 
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
#   Areas. Do not modify the strings `*_ID`
#

TEXT_AREA_POWER_BUTTON_ID = 'PB'
TEXT_DESCRIPTION_POWER_BUTTON = "Power Button"

TEXT_AREA_POWER_BUTTON_EYES_ID = 'PBE'
TEXT_DESCRIPTION_ALIENWAREWARE_POWERBUTTON_EYES = "Power Button: Eyes"

TEXT_AREA_MEDIA_BAR_ID = 'MB'
TEXT_DESCRIPTION_MEDIA_BAR = "Media Bar"

TEXT_AREA_TOUCH_PAD_ID = 'TP'
TEXT_DESCRIPTION_TOUCHPAD = "Touchpad"

TEXT_AREA_ALIENWARE_LOGO_ID = 'AL'
TEXT_DESCRIPTION_ALIENWAREWARE_LOGO = "Logo"

TEXT_AREA_ALIENWARE_HEAD_ID = 'AH'
TEXT_DESCRIPTION_ALIENWAREWARE_HEAD = "Head"

TEXT_AREA_ALIENWARE_OUTER_LID_ID = 'OI'
TEXT_DESCRIPTION_OUTER_LID = "Outer Lid"

TEXT_AREA_LEFT_SPEAKER_ID = 'LS'
TEXT_DESCRIPTION_LEFT_SPEAKER = "Speaker: Left"

TEXT_AREA_RIGHT_SPEAKER_ID = 'RS'
TEXT_DESCRIPTION_RIGHT_SPEAKER = "Speaker: Right"

TEXT_AREA_LEFT_KEYBOARD_ID = 'LK'
TEXT_DESCRIPTION_LEFT_KEYBOARD = "Keyboard: Left "

TEXT_AREA_LEFT_CENTER_KEYBOARD_ID = 'LCK'
TEXT_DESCRIPTION_LEFT_CENTER_KEYBOARD = "Keyboard: Left-Center"

TEXT_AREA_RIGHT_CENTER_KEYBOARD_ID = 'RCK'
TEXT_DESCRIPTION_RIGHT_CENTER_KEYBOARD = "Keyboard: Righ-Center"

TEXT_AREA_RIGHT_KEYBOARD_ID = 'RK'
TEXT_DESCRIPTION_RIGHT_KEYBOARD = "Keyboard: Right"

TEXT_AREA_KEYBOARD_ID = 'KB'
TEXT_DESCRIPTION_KEYBOARD = "Keyboard"

TEXT_AREA_LIGHT_PIPE_ID = 'LP'
TEXT_DESCRIPTION_LIGHT_PIPE = "Pipe: Left"

TEXT_AREA_TACTX_ID = 'TX'
TEXT_DESCRIPTION_TACTX = "Tact-X"

TEXT_AREA_HARD_DISK_DRIVE_ID = 'HDD'
TEXT_DESCRIPTION_HDD = "Hard Disk Drive"

TEXT_AREA_WIFI_ID = 'WF'
TEXT_DESCRIPTION_WIFI = "Wifi"

TEXT_AREA_CAPS_LOCK_ID = 'CL'
TEXT_DESCRIPTION_CAPS_LOCK = "Caps Lock"

TEXT_AREA_BOOT_ID = 'BT'
TEXT_DESCRIPTION_BOOT = "Boot"

TEXT_AREA_STANDBY_ID = 'SB'
TEXT_DESCRIPTION_STAND_BY = "StandBy"

TEXT_AREA_AC_POWER_ID = 'AC'
TEXT_DESCRIPTION_AC_POWER = "AC Power"

TEXT_AREA_ON_BATTERY_ID = 'BAT'
TEXT_DESCRIPTION_ON_BATTERY = "On Battery"

TEXT_AREA_CHARGING_ID = 'CH'
TEXT_DESCRIPTION_CHARGING = "Charging"


#
#    Computer Names
#
TEXT_AURORAR4 = "AuroraR4"
TEXT_M11XR1 = 'M11XR1'
TEXT_M11XR2 = 'M11XR2'
TEXT_M11XR3 = 'M11XR3'
TEXT_M11XR25 = 'M11XR25'
TEXT_M14XR1 = 'M14XR1'
TEXT_M14XR2 = 'M14XR2'
TEXT_M14XR3 = 'M14XR3'
TEXT_M17X = 'M17X'
TEXT_M17XR2 = 'M17XR2'
TEXT_M17XR3 = 'M17XR3'
TEXT_M18XRX = 'M18XRX'
TEXT_M18XR2 = 'M18XR2'
TEXT_M15XAREA51 = 'M15XArea51'
TEXT_ALIENWAREWARE13 = 'Alienware13'
TEXT_ALIENWAREWARE13R3 = 'Alienware13R3'
TEXT_ALIENWAREWARE15 = 'Alienware15'
TEXT_ALIENWAREWARE15R3 = 'Alienware15R3'
