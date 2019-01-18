#!/usr/bin/python3
#

#  Copyright (C) 2019  Rafael Senties Martinelli
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


import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk

import os
import subprocess

from AKBL.texts import (TEXT_ONLY_ROOT)
from AKBL.utils import getuser
from AKBL.Paths import Paths; _SOFTWARE_PATHS = Paths()
from AKBL.Engine.Driver import Driver

import AKBL.Data.Computer.factory as computer_factory

from AKBL.Addons.gtk_utils import gtk_dialog_info, gtk_dialog_question
from AKBL.Addons.ModelChooser.texts import _TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT

_EMPTY_MODEL="<NONE>"

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
        builder = Gtk.Builder()
        builder.add_from_file(_SOFTWARE_PATHS._model_chooser_glade_file)
        builder.connect_signals(self)
        
        
        self.window_model_chooser = builder.get_object('window_model_chooser')
        self.treeview_computer_models = builder.get_object('treeview_computer_models')
        self.liststore_computer_models = builder.get_object('liststore_computer_models')
        self.label_detected_as = builder.get_object('label_detected_as')
        self.label_set_as = builder.get_object('label_set_as')
        self.textbuffer_computer_data = builder.get_object('textbuffer_computer_data')
        
        """
            
        """
        #
        #
        
        self.upadte_detected_as()
        self.update_set_computer()
        self.update_models_liststore()
        self.textbuffer_computer_data.set_text(get_alienware_device_info())
        print("The current configuration is: "+self._get_default_computer_name())
        
        """
        
        """
        self.window_model_chooser.show_all()
    

    
    def update_models_liststore(self):
        
        default_computer_name = self._get_default_computer_name()
        driver = Driver()
        
        self.liststore_computer_models.clear()
        for computer in computer_factory.get_computers():
            is_selected = computer.NAME == default_computer_name
            driver.load_device(computer.VENDOR_ID, computer.PRODUCT_ID)
            
            self.liststore_computer_models.append([computer.NAME, is_selected, True, driver.has_device()])
    
    
    def upadte_detected_as(self):
        driver = Driver()
        driver.find_device()
        
        if driver.has_device():
            self.label_detected_as.set_text(driver.computer.NAME)
        else:
            self.label_detected_as.set_text(_EMPTY_MODEL)
    
    def update_set_computer(self):
        self.label_set_as.set_text(self._get_default_computer_name())
    
    
    def _on_model_change_clicked(self, widget, clicked_row):
        
        clicked_row = int(clicked_row)
        
        for i, _ in enumerate(self.liststore_computer_models):
            
            iter_row = self.liststore_computer_models.get_iter(i)
              
            if i != clicked_row:
                self.liststore_computer_models.set_value(iter_row, 1, False)
            else:
                self.liststore_computer_models.set_value(iter_row, 1, True)
                computer_model = self.liststore_computer_models.get_value(iter_row, 0)
                computer_factory.set_default_computer(computer_model)
        
        
        self.update_set_computer()
        
            
    def _get_default_computer_name(self):
    
        default_computer = computer_factory.get_default_computer()
        
        if default_computer is None:
            return _EMPTY_MODEL
        else:
            return default_computer.NAME
        
    def _on_button_close_clicked(self, data=None):
        
        if self.label_set_as.get_text() == _EMPTY_MODEL:
            if gtk_dialog_question(None, 
                                   _TEXT_NO_COMPUTER_MODEL_WANT_TO_QUIT, 
                                   icon=_SOFTWARE_PATHS._small_icon_file):
                return
                
        
        Gtk.main_quit()
    
    def on_window_destroy(self, data=None):
        Gtk.main_quit()

def main():
    
    if getuser() != 'root':
        gtk_dialog_info(None, TEXT_ONLY_ROOT, icon=_SOFTWARE_PATHS._small_icon_file)
        exit()
    else:
        
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
        ModelChooser()
        Gtk.main()
