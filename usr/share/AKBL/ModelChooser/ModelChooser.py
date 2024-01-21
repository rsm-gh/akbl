#!/usr/bin/python3
#

#  Copyright (C) 2019, 2024 Rafael Senties Martinelli.
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

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from AKBL.Paths import Paths
from AKBL.utils import get_alienware_device_info
import AKBL.Computer.factory as computer_factory

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

from gtk_utils import gtk_dialog_question

_EMPTY_MODEL = "<NONE>"
_SOFTWARE_PATHS = Paths()
_TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT = '''
No computer model is chosen. If you quit without
choosing a computer the software will not work. 

Do you want to go back?
'''

class ModelChooser(Gtk.Window):

    def __init__(self):

        """
            Glade
        """
        glade_path = os.path.join(SCRIPT_DIR, "ModelChooser.glade")
        builder = Gtk.Builder()
        builder.add_from_file(glade_path)
        builder.connect_signals(self)

        self.window_model_chooser = builder.get_object('window_model_chooser')
        self.treeview_hardware_comp = builder.get_object('treeview_hardware_comp')
        self.liststore_hardware_comp = builder.get_object('liststore_hardware_comp')
        self.treeview_hardware_not_comp = builder.get_object('treeview_hardware_not_comp')
        self.liststore_hardware_not_comp = builder.get_object('liststore_hardware_not_comp')
        self.textbuffer_computer_data = builder.get_object('textbuffer_computer_data')
        self.__populate_liststores()
        self.textbuffer_computer_data.set_text(get_alienware_device_info())

        """
        
        """
        self.window_model_chooser.show_all()

    def __populate_liststores(self):

        installed_computer_name = self.__get_installed_computer_name()

        self.liststore_hardware_comp.clear()
        self.liststore_hardware_not_comp.clear()

        compatible_computers = computer_factory.get_compatible_computers()

        for inst_computer in computer_factory.get_installed_computers():

            if inst_computer in compatible_computers:
                    self.liststore_hardware_comp.append([inst_computer.name,
                                                         inst_computer.name == installed_computer_name,
                                                         True])
            else:
                self.liststore_hardware_not_comp.append([inst_computer.name])

    def _on_model_change_clicked(self, _, clicked_row):

        clicked_row = int(clicked_row)

        for i, _ in enumerate(self.liststore_hardware_comp):
            iter_row = self.liststore_hardware_comp.get_iter(i)
            self.liststore_hardware_comp.set_value(iter_row, 1, i == clicked_row)


    @staticmethod
    def __get_installed_computer_name():

        default_computer = computer_factory.get_installed_computer()

        if default_computer is None:
            return _EMPTY_MODEL
        else:
            return default_computer.name

    def _on_button_close_clicked(self, *_):

        #
        # Install the selected configuration
        #
        for i, _ in enumerate(self.liststore_hardware_comp):

            iter_row = self.liststore_hardware_comp.get_iter(i)

            if self.liststore_hardware_comp.get_value(iter_row, 1):
                computer_model = self.liststore_hardware_comp.get_value(iter_row, 0)
                computer_factory.set_installed_computer(computer_model)
                break

        #
        # Retrieve the installed configuration
        #
        installed_computer_name = self.__get_installed_computer_name()

        #
        # Warn the user that no computer is installed
        #
        if installed_computer_name == _EMPTY_MODEL:
            if gtk_dialog_question(None, _TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT, icon=_SOFTWARE_PATHS._icon_file):
                return


        #
        # Print the computer model
        #
        print("The installed computer model is:", installed_computer_name)

        #
        # Quit the application
        #
        
        Gtk.main_quit()

    def on_window_destroy(self, *_):
        self._on_button_close_clicked()

if __name__ == "__main__":
    _ = ModelChooser()
    Gtk.main()
