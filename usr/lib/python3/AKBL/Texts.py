#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
#
#
#  AKBL is free software; you can redistribute it and/or modify
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

class Texts:
    class Indicator:
        profiles = "Profiles"
        start_gui = "GUI"
        switch_state = "Switch State"
        exit = "Exit"
        lights_on = "On"
        lights_off = "Off"
        no_daemon = "No Daemon"

    class Commands:
        _daemon_off = "Error: The daemon is off or the connection couldn't be established."
        _wrong_argument = '''Error: wrong argument. use "akbl --help"'''
        _help = '''
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
        _license = '''
  Copyright (C) 2014-2024 Rafael Senties Martinelli.
                2011-2012 the pyAlienFX team.

  AKBL is free software; you can redistribute it and/or modify
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

    class GUI:

        _maximum_zones = "You have reached the maximum number of AreaItems for the {}."
        _add = "Add"
        _theme_choose_folder = "Choose a folder to export the theme"
        _theme_confirm_delete = "Are you sure that you want to delete {}?"
        _theme_choose = "Choose an AKBL theme"
        _theme_duplicate = "A theme with this name already exists. Do you want to overwrite it?"
        _theme_must_saved = "The theme {} must be saved before applying it."
        _no_computer_title = "Undefined Computer"
        _no_computer = 'It is mandatory to select a computer model. Run as root \n"akbl --model-chooser-gui".'