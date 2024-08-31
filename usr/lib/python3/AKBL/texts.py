#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
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

_TEXT_HELP = '''
Usage:

    akbl <option>

 Options:

    --on                              Turn on the computer lights.
    --off                             Turn off the computer lights.
    --switch                          Switch the computer lights on/off.
    --set-theme <theme_name>          Set the selected theme (on).
    
    --model-chooser-gui               Launch the model chooser from a GUI.
    --model-chooser-cmd               Launch the model chooser from a CMD.
    
    --start-indicator                 Start the indicator.
    --start-white-indicator           Start the indicator (with white icons).
    
    --start-daemon                    Start the Daemon.
    --ping                            Check if the Daemon is connected and ready to execute commands.
    
    --block-testing                   Launch the block testing window.
    
    -h, --help                        Display this dialog.
    -v, --version                     Display the software version.  
    -l, --license                     Display the software license.

 *If no option is introduced the graphical interface is launched.
'''

_TEXT_LICENSE = '''
  Copyright (C) 2014-2019, 2024 Rafael Senties Martinelli.
                2011-2012 the pyAlienFX team.

  This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License 3 as published by
   the Free Software Foundation.

  This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software Foundation,
   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 '''

_TEXT_ADD = "Add"

_TEXT_CHOOSE_A_FOLDER_TO_EXPORT = "Choose a folder to export the theme"
_TEXT_CHOOSE_A_THEME = "Choose an AKBL theme"
_TEXT_THEME_ALREADY_EXISTS = '''There's already a theme with this filename,
do you want to overwrite it?'''

_TEXT_COPY_CONFIG = '''It seems that there was an existing AKBL
configuration, probably made by an older version.

Do you want to import it for this user? (yes)
'''


class Texts:
    class Indicator:
        profiles = "Profiles"
        start_gui = "GUI"
        switch_state = "Switch State"
        exit = "Exit"
        lights_on = "On"
        lights_off = "Off"
        no_daemon = "No Daemon"


_TEXT_ERROR_DAEMON_OFF = "Error: The daemon is off or the connection couldn't be established."
_TEXT_WRONG_ARGUMENT = '''Error: wrong argument. use "akbl --help"'''
_TEXT_APPLYING_CONFIGURATION = "Applying the configuration.."
_TEXT_SHUTTING_LIGHTS_OFF = "Shutting the lights off.."
_TEXT_TURNING_LIGHTS_ON = "Turning the lights on.."
_TEXT_THE_GUI_NEEDS_ROOT = "The graphical interface needs to be run as root."
_TEXT_GUI_CANT_DAEMON_OFF = "The GUI can not start because the daemon is off."
_TEXT_SAVING_THE_CONFIGURATION = "Saving the configuration.."
_TEXT_CONFIGURATION_DELETED = "The configuration has been deleted.."
_TEXT_CONFIRM_DELETE_CONFIGURATION = "Are you sure that you want to\n delete this configuration?"
_TEXT_MAXIMUM_NUMBER_OF_ZONES_REACHED = "You have reached the maximum number of AreaItems for the {}."
