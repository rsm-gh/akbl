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
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from AKBL.Paths import Paths
from AKBL.utils import getuser
from AKBL.texts import TEXT_ONLY_ROOT
import AKBL.Computer.factory as computer_factory

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

from gtk_utils import gtk_dialog_info, gtk_dialog_question

_EMPTY_MODEL = "<NONE>"
_SOFTWARE_PATHS = Paths()
_TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT = '''
No computer model is chosen. If you quit without
choosing a computer the software will not work. 

Do you want to go back?
'''

def get_alienware_device_info():
    bash_output = subprocess.run("lsusb",
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 universal_newlines=True)

    device_info = str(bash_output.stdout)

    for line in device_info.split("\n"):

        if "Alienware" in line:
            bus_id = line.split()[1]
            device_id = line.split()[3][:-1]

            bash_output = subprocess.run("lsusb -D /dev/bus/usb/{}/{} 2>/dev/null".format(bus_id, device_id),
                                         shell=True,
                                         stdout=subprocess.PIPE,
                                         universal_newlines=True)

            device_info = str(bash_output.stdout)
            break

    return device_info


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

        self.__default_computer_name = self.__get_default_computer_name()

        self.__populate_liststores()
        self.textbuffer_computer_data.set_text(get_alienware_device_info())
        print("The current configuration is: " + self.__get_default_computer_name())

        """
        
        """
        self.window_model_chooser.show_all()

    def __populate_liststores(self):

        self.liststore_hardware_comp.clear()
        self.liststore_hardware_not_comp.clear()

        compatible_computers = computer_factory.get_compatible_computers()

        for inst_computer in computer_factory.get_compatible_computers():

            if inst_computer in compatible_computers:
                    self.liststore_hardware_comp.append([inst_computer.name,
                                                         inst_computer.name == self.__default_computer_name,
                                                         True])
            else:
                self.liststore_hardware_not_comp.append([inst_computer.name])

    def _on_model_change_clicked(self, _, clicked_row):

        clicked_row = int(clicked_row)

        for i, _ in enumerate(self.liststore_hardware_comp):

            iter_row = self.liststore_hardware_comp.get_iter(i)

            if i != clicked_row:
                self.liststore_hardware_comp.set_value(iter_row, 1, False)
            else:
                self.liststore_hardware_comp.set_value(iter_row, 1, True)
                computer_model = self.liststore_hardware_comp.get_value(iter_row, 0)
                computer_factory.set_installed_computer(computer_model)

    @staticmethod
    def __get_default_computer_name():

        default_computer = computer_factory.get_installed_computer()

        if default_computer is None:
            return _EMPTY_MODEL
        else:
            return default_computer.name

    def _on_button_close_clicked(self, *_):

        #
        # Do not exit if no computer has been set (warn the user)
        #
        if self.__get_default_computer_name() == _EMPTY_MODEL:
            if gtk_dialog_question(None, _TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT, icon=_SOFTWARE_PATHS._small_icon_file):
                return

        #
        # In case that the computer is the same (as previously used), update the file
        #

        if self.__default_computer_name == self.__get_default_computer_name():

            for i, _ in enumerate(self.liststore_hardware_comp):

                iter_row = self.liststore_hardware_comp.get_iter(i)

                if self.liststore_hardware_comp.get_value(iter_row, 1):
                    computer_model = self.liststore_hardware_comp.get_value(iter_row, 0)
                    computer_factory.set_installed_computer(computer_model)

                    break

        #
        # Quit the application
        #

        Gtk.main_quit()

    def on_window_destroy(self, *_):
        self._on_button_close_clicked()

if __name__ == "__main__":
    if getuser() != 'root':
        gtk_dialog_info(None, TEXT_ONLY_ROOT, icon=_SOFTWARE_PATHS._small_icon_file)
        exit()

    _ = ModelChooser()
    Gtk.main()
