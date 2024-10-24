#!/usr/bin/python3
#

#  Copyright (C) 2019-2024 Rafael Senties Martinelli.
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
from AKBL.console_printer import print_info
import AKBL.Computer.factory as computer_factory

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

_EMPTY_MODEL = "<NONE>"
_AKBL_PATHS = Paths()


class ModelChooser(Gtk.Window):

    def __init__(self):
        super().__init__()

        """
            Glade
        """
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(SCRIPT_DIR, "ModelChooser.glade"))
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

        installed_computer_name = self.__get_default_computer_name()

        self.liststore_hardware_comp.clear()
        self.liststore_hardware_not_comp.clear()

        compatible_computers = computer_factory.get_compatible_computers()

        for inst_computer in computer_factory.get_all_computers():

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
    def __get_default_computer_name():

        default_computer = computer_factory.get_default_computer()

        if default_computer is None:
            return _EMPTY_MODEL
        else:
            return default_computer.name

    def on_window_destroy(self, *_):
        """
            I removed the code to warn the user if no computer is selected, because
            it was not possible to get the GUI back.
        """

        #
        # Install the selected configuration
        #
        for i, _ in enumerate(self.liststore_hardware_comp):

            iter_row = self.liststore_hardware_comp.get_iter(i)

            if self.liststore_hardware_comp.get_value(iter_row, 1):
                computer_model = self.liststore_hardware_comp.get_value(iter_row, 0)
                computer_factory.set_default_computer(computer_model)
                break

        #
        # Retrieve the installed configuration
        #
        installed_computer_name = self.__get_default_computer_name()

        #
        # Print the computer model
        #
        print_info(f"The installed computer model is: {installed_computer_name}")

        #
        # Quit the application
        #

        Gtk.main_quit()



if __name__ == "__main__":
    _ = ModelChooser()
    Gtk.main()
