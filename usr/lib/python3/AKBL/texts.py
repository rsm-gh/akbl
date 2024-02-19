#!/usr/bin/python3
#

#  Copyright (C) 2014-2019, 2024 Rafael Senties Martinelli.
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

TEXT_HELP = '''
Usage:

    akbl <option>

 Options:

    --change                          Change the computer lights on/off.
    --on                              Turn on the computer lights.
    --off                             Turn off the computer lights.
    --set-profile <profile_name>      Turn on the selected profile.
    
    --model-chooser-gui               Launch the model chooser from a GUI.
    --model-chooser-cmd               Launch the model chooser from a CMD.
    
    --start-indicator                 Start the indicator.
    --start-white-indicator           Start the indicator (with white icons).
    
    --start-daemon                    Start the daemon.
    --daemon-is-on                    Return weather the daemon is running or not.
    
    --block-testing                   Launch the block testing window.
    
    -h, --help                        Display this dialog.
    -v, --version                     Display the software version.  
    -l, --license                     Display the software license.

 *If no option is introduced the graphical interface is launched.
'''

TEXT_LICENSE = '''
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

TEXT_ADD = "Add"

TEXT_CHOOSE_A_FOLDER_TO_EXPORT = "Choose a folder to export the theme"
TEXT_CHOOSE_A_THEME = "Choose an alienware-kbl theme"
TEXT_THEME_ALREADY_EXISTS = '''There's already a theme with this filename,
do you want to overwrite it?'''


TEXT_COPY_CONFIG = '''It seems that there was an existing alienware-kbl
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


TEXT_ERROR_DAEMON_OFF = "The daemon is off or the connection couldn't be established."

TEXT_WRONG_ARGUMENT = '''akbl: wrong argument. use "akbl --help"'''

TEXT_APPLYING_CONFIGURATION = "Applying the configuration.."

TEXT_SHUTTING_LIGHTS_OFF = "Shutting the lights off.."

TEXT_TURNING_LIGHTS_ON = "Turning the lights on.."

TEXT_THE_GUI_NEEDS_ROOT = "The graphical interface needs to be run as root."

TEXT_GUI_CANT_DAEMON_OFF = "The GUI can not start because the daemon is off."

TEXT_SAVING_THE_CONFIGURATION = "Saving the configuration.."

TEXT_CONFIGURATION_DELETED = "The configuration has been deleted.."

TEXT_CONFIRM_DELETE_CONFIGURATION = "Are you sure that you want to\n delete this configuration?"

TEXT_MAXIMUM_NUMBER_OF_ZONES_REACHED = "You have reached the maximum number of Zones for the {}."
