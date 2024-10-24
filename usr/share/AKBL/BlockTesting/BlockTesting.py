#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
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


import gi
import os
import sys
from traceback import format_exc

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from AKBL.Computer.Computer import Computer
from AKBL.Engine.Driver import Driver
from AKBL.Engine.Command import Command
from AKBL.Engine.Controller import Controller
from AKBL.utils import get_alienware_device_info, rgb_to_hex

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_PROJECT_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _PROJECT_DIR)

from gtk_utils import gtk_dialog_info, gtk_append_text_to_buffer

_TEXT_DEVICE_NOT_FOUND = '''[Device not found]: Vendor ID: {}\t Product ID: {}\n'''
_TEXT_DEVICE_FOUND = '''[Device found]: Vendor ID: {}\t Product ID: {}\n'''
_TEXT_BLOCK_TEST = '''[TEST]: areaitem: {}\t mode:{}\t speed:{}\t color1:{}\t color2: {}\n'''
_TEXT_BLOCK_LIGHTS_OFF = '''[Command]: Lights off'''


class BlockTesting(Gtk.Window):

    def __init__(self):
        super().__init__()
        self.__computer = Computer()
        self.__driver = Driver()
        self.__controller = None
        self.__computer_blocks_to_save = []

        """
            Glade
        """
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(_SCRIPT_DIR, "BlockTesting.glade"))
        builder.connect_signals(self)

        glade_object_names = (
            'window_block_testing',
            'entry_id_vendor',
            'entry_id_product',
            'button_connect',
            'box_block_testing',
            'spinbutton_block_speed',
            'viewport_common_block',
            'button_update_common_blocks',
            'button_block_make_test',
            'checkbutton_auto_turn_off',
            'checkbutton_hex_format_when_finding',
            'combobox_block_modes',
            'colorbutton_1_block',
            'colorbutton_2_block',
            'config_grid',
            'textbuffer_device_info',
            'combobox_default_blocks',
            'textbuffer_block_testing',
            'entry_block_testing',
            'box_pyusb',
            'textbuffer_pyusb',
            'entry_custom_command',
            'button_send_custom_command')

        # load the glade objects
        for glade_object in glade_object_names:
            setattr(self, glade_object, builder.get_object(glade_object))

        # get the computer info
        computer_device_info = get_alienware_device_info()

        # Fill the computer data
        self.textbuffer_device_info.set_text(computer_device_info)

        # Fill the idProduct and idVendor entries if possible
        if 'idVendor' in computer_device_info and 'idProduct' in computer_device_info:
            for line in computer_device_info.split('\n'):
                if 'idVendor' in line:
                    self.entry_id_vendor.set_text(line.split()[1].strip())
                elif 'idProduct' in line:
                    self.entry_id_product.set_text(line.split()[1].strip())

        # Display the window
        self.window_block_testing.show_all()

    def on_entry_block_testing_changed(self, entry, *_):
        text = entry.get_text()
        try:
            value = int(text)

            if value < 0:
                self.button_block_make_test.set_sensitive(False)
            else:
                self.button_block_make_test.set_sensitive(True)

        except Exception:
            self.button_block_make_test.set_sensitive(False)

    def on_button_connect_clicked(self, *_):

        hex_format = self.checkbutton_hex_format_when_finding.get_active()

        try:
            if hex_format:
                vendor = int(self.entry_id_vendor.get_text(), 16)  # this is because it's a  string
                product = int(self.entry_id_product.get_text(), 16)  # this is because it's a string
            else:
                vendor = int(self.entry_id_vendor.get_text())
                product = int(self.entry_id_product.get_text())

        except ValueError:
            if hex_format:
                text = "Only HEX numbers can be entered."
            else:
                text = "Only Integer numbers can be entered."

            gtk_dialog_info(self.window_block_testing, text)
            return

        #
        # try to load the driver
        #
        self.__driver.load_device(id_vendor=vendor, id_product=product)

        #
        # Check the controller
        #
        if not self.__driver.has_device():
            gtk_append_text_to_buffer(self.textbuffer_block_testing, _TEXT_DEVICE_NOT_FOUND.format(vendor, product))
            gtk_dialog_info(self.window_block_testing, "The connection was not successful.")
            self.box_block_testing.set_sensitive(False)
            self.box_pyusb.set_sensitive(False)
            self.entry_id_vendor.set_sensitive(True)
            self.entry_id_product.set_sensitive(True)
            return

        gtk_dialog_info(self.window_block_testing, "The connection was successful.")
        self.button_connect.set_sensitive(False)

        self.__computer.vendor_id = vendor
        self.__computer.product_id = product

        self.__controller = Controller(self.__computer)

        self.__computer_blocks_to_save = (
            # (True, self.__computer.block_load_on_boot),
            # (True, self.__computer.BLOCK_STANDBY),
            # (True, self.__computer.block_ac_power),
            # (#True, self.__computer.block_charging),
            # (True, self.__computer.block_battery_sleeping),
            # (True, self.__computer.block_battery_power),
            # (True, self.__computer.block_battery_critical),
            (False, self.__computer.block_load_on_boot),)

        # Add the general computer variables
        row_index = 0
        for attr_name, attr_value in sorted(vars(self.__computer).items()):
            if not attr_name.startswith("_") and isinstance(attr_value, int):
                label = Gtk.Label(label=attr_name)
                label.set_xalign(0)

                adjustment = Gtk.Adjustment(0, 0, 9999999999999, 1, 1, 0)
                spinbutton = Gtk.SpinButton()
                spinbutton.set_adjustment(adjustment)
                spinbutton.set_value(attr_value)
                spinbutton.set_digits(0)
                spinbutton.set_numeric(True)

                spinbutton.connect("value-changed", self.on_dynamic_spin_general_properties_changed, attr_name)

                self.config_grid.attach(label, 0, row_index, 1, 1)
                self.config_grid.attach(spinbutton, 1, row_index, 1, 1)
                row_index += 1

            self.config_grid.show_all()

            # activate the window
            self.box_block_testing.set_sensitive(True)
            self.box_pyusb.set_sensitive(True)
            self.entry_id_vendor.set_sensitive(False)
            self.entry_id_product.set_sensitive(False)
            gtk_append_text_to_buffer(self.textbuffer_block_testing, _TEXT_DEVICE_FOUND.format(vendor, product))
            self.combobox_default_blocks.set_active(0)

    def on_button_send_custom_command_clicked(self, *_):

        command_value = self.entry_custom_command.get_text()

        try:
            values = (int(val) for val in command_value.split(":"))
        except Exception:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n' + "WRONG FORMAT" + '\n')
            return

        constructor = (Command("Custom", values),)

        try:
            self.__driver.write_constructor(constructor)
        except Exception:
            gtk_append_text_to_buffer(self.textbuffer_pyusb, '\n' + format_exc() + '\n')
            return

        gtk_append_text_to_buffer(self.textbuffer_pyusb, command_value + "\n")

    def on_button_block_make_test_clicked(self, button, *_):

        if self.checkbutton_auto_turn_off.get_active():
            self.on_button_block_testing_lights_off_clicked(button)

        try:
            areaitem_left_color = self.colorbutton_1_block.get_color()
            areaitem_left_color = rgb_to_hex([areaitem_left_color.red / 65535.0,
                                          areaitem_left_color.green / 65535.0,
                                          areaitem_left_color.blue / 65535.0])

            areaitem_right_color = self.colorbutton_2_block.get_color()
            areaitem_right_color = rgb_to_hex([areaitem_right_color.red / 65535.0,
                                           areaitem_right_color.green / 65535.0,
                                           areaitem_right_color.blue / 65535.0])

            areaitem_block = int(self.entry_block_testing.get_text())
            speed = self.spinbutton_block_speed.get_value_as_int()

            index = self.combobox_block_modes.get_active()
            model = self.combobox_block_modes.get_model()
            areaitem_mode = model[index][0]
            areaitem_mode = areaitem_mode.lower()

            # Log the test
            #
            gtk_append_text_to_buffer(self.textbuffer_block_testing, _TEXT_BLOCK_TEST.format(areaitem_block,
                                                                                             areaitem_mode,
                                                                                             speed,
                                                                                             areaitem_left_color,
                                                                                             areaitem_right_color))

            #   Test
            #
            self.__controller.clear_constructor()

            for save, block in self.__computer_blocks_to_save:
                self.__controller.add_block_line(save=save, block=block)
                self.__controller.add_reset_line(self.__computer.reset_all_lights_on)
                self.__controller.add_speed_line(speed)
                self.__controller.add_color_line(areaitem_block, areaitem_mode, areaitem_left_color, areaitem_right_color)
                self.__controller.end_colors_line()
                self.__controller.end_block_line()

            self.__controller.apply_config()

        except Exception:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n' + format_exc() + '\n')

    def on_button_block_testing_lights_off_clicked(self, *_):
        try:

            self.__controller.clear_constructor()

            for save, block in self.__computer_blocks_to_save:
                self.__controller.add_block_line(save, block)
                self.__controller.add_reset_line(self.__computer.reset_all_lights_off)

            self.__controller.apply_config()

            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n' + _TEXT_BLOCK_LIGHTS_OFF + '\n')

        except Exception:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n' + format_exc())

    def on_checkbutton_protect_common_blocks_clicked(self, checkbutton, *_):
        if checkbutton.get_active():
            self.viewport_common_block.set_sensitive(False)
        else:
            self.viewport_common_block.set_sensitive(True)

    def on_combobox_default_blocks_changed(self, combobox, *_):
        index = combobox.get_active()
        model = combobox.get_model()
        value = model[index][0]

        if value == -1:
            self.entry_block_testing.set_sensitive(True)
        else:
            self.entry_block_testing.set_sensitive(False)
            self.entry_block_testing.set_text(str(value))

    def on_dynamic_spin_general_properties_changed(self, spin, variable_name):
        value = spin.get_value_as_int()
        setattr(self.__computer, variable_name, value)
        gtk_append_text_to_buffer(self.textbuffer_block_testing, "\n {} = {}".format(variable_name, value))

    @staticmethod
    def on_window_block_testing_destroy(*_):
        Gtk.main_quit()


if __name__ == "__main__":
    _ = BlockTesting()
    Gtk.main()
