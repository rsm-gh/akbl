#!/usr/bin/python3
#

#  Copyright (C)  2014-2019  Rafael Senties Martinelli
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



TEXT_HELP = '''
Usage:

    akbl <option>

 Options:

    --change                          Change the computer lights on/off.
    --on                              Turn on the computer lights.
    --off                             Turn off the computer lights.
    --set-profile <profile_name>      Turn on the selected profile.
    
    --model-chooser                   Start the model chooser.
    
    --start-indicator                 Start the indicator.
    
    --start-daemon                    Start the daemon.
    --daemon-is-on                    Return weather the daemon is running or not.
    
    --block-testing                   Display the block testing window.
    
    -h, --help                        Display this dialog.
    -v, --version                     Display the software version.  
    -l, --license                     Display the software license.

 *If no option is introduced the graphical interface is launched.
'''

TEXT_LICENSE = '''
  Copyright (C) 2014-2019  Rafael Senties Martinelli
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


TEXT_ERROR_DAEMON_OFF = "The daemon is off or the connection couldn't be stablished."

TEXT_WRONG_ARGUMENT = '''alienware-kbl: wrong argument. use "alienware-kbl --help"'''

TEXT_RESTART_THE_SYSTEM = "{0} You will have to restart the system to make it effective."

TEXT_ONLY_FROM_TERMINAL = "** The root permission has been removed. Unfortunately,\nthe launcher will still asking for it. call it from the terminal to skip it. **\n\n"

TEXT_APPLYING_CONFIGURATION = "Applying the configuration.."

TEXT_SHUTTING_LIGHTS_OFF = "Shutting the lights off.."

TEXT_TURNING_LIGHTS_ON = "Turning the lights on.."

TEXT_THE_GUI_NEEDS_ROOT = "The graphical interface needs to be run as root."

TEXT_GUI_CANT_DAEMON_OFF = "The GUI can not start because the daemon is off."

TEXT_SAVING_THE_CONFIGURATION = "Saving the configuration.."

TEXT_CONFIGURATION_DELETED = "The configuration has been deleted.."

TEXT_CONFIRM_DELETE_CONFIGURATION = "Are you sure that you want to\n delete this configuration?"

TEXT_MAXIMUM_NUMBER_OF_ZONES_REACHED = "You have reached the maximum number of Zones for the {}."

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
TEXT_BLOCK_TEST = '''[TEST]: zone: {}\t mode:{}\t speed:{}\t color1:{}\t color2: {}\n'''
TEXT_BLOCK_LIGHTS_OFF = '''[Command]: Lights off'''
