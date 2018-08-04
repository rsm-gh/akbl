#!/usr/bin/python3
#

#  Copyright (C) 2014-2018  Rafael Senties Martinelli 
#                2011-2012  the pyAlienFX team
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
from gi.repository import Gtk, GObject, Gdk

import os
import threading
import shutil
from traceback import format_exc
from time import sleep
from copy import deepcopy

import AKBL.Configuration.Theme as Theme
import AKBL.Configuration.Computers as Computer
from AKBL.utils import print_error, print_warning
from AKBL.Bindings import Bindings
from AKBL.Configuration.CCParser import CCParser
from AKBL.Configuration.Paths import Paths
from AKBL.ADDONS.GUI.ZoneWidget import ZoneWidget
from AKBL.texts import (TEXT_COPY_CONFIG, 
                        TEXT_COMPUTER_DATA, 
                        TEXT_ADD, 
                        TEXT_CONFIRM_DELETE_CONFIGURATION, 
                        TEXT_CONFIGURATION_DELETED,
                        TEXT_SHUTTING_LIGHTS_OFF,
                        TEXT_APPLYING_CONFIGURATION,
                        TEXT_SAVING_THE_CONFIGURATION,
                        TEXT_THEME_ALREADY_EXISTS,
                        TEXT_CHOOSE_A_THEME,
                        TEXT_CHOOSE_A_FOLDER_TO_EXPORT)

os.chdir(Paths().MAIN) # this is important for the rest of the code.

def get_text_gtk_buffer(textbuffer):
    return textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), True)

def gtk_append_text_to_buffer(textbuffer, text):
    textbuffer.set_text(get_text_gtk_buffer(textbuffer) + text)


def gtk_dialog_question(parent, text1, text2=None, icon=None):

    dialog = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, text1)

    if icon is not None:
        dialog.set_icon_from_file(icon)

    if text2 is not None:
        dialog.format_secondary_text(text2)

    response = dialog.run()
    if response == Gtk.ResponseType.YES:
        dialog.hide()
        return True

    elif response == Gtk.ResponseType.NO:
        dialog.hide()
        return False


def gtk_dialog_info(parent, text1, text2=None, icon=None):

    dialog = Gtk.MessageDialog(parent, Gtk.DialogFlags.MODAL, Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, text1)

    if icon is not None:
        dialog.set_icon_from_file(icon)

    if text2 is not None:
        dialog.format_secondary_text(text2)

    _ = dialog.run()
    dialog.destroy()


def gtk_file_chooser(parent, title='', icon_path=None, default_folder=None, filters=[]):

    window = Gtk.FileChooserDialog(title, parent, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL,
                                                                                 Gtk.ResponseType.CANCEL,
                                                                                 Gtk.STOCK_OPEN,
                                                                                 Gtk.ResponseType.OK))

    window.set_default_response(Gtk.ResponseType.NONE)
    window.set_transient_for(parent)

    if icon_path is not None:
        window.set_icon_from_file(icon_path)

    if default_folder is not None:
        window.set_current_folder(default_folder)

    for filter_name, filter_extension in filters:
        gtk_filter = Gtk.FileFilter()
        gtk_filter.set_name(filter_name)
        gtk_filter.add_pattern(filter_extension)
        window.add_filter(gtk_filter)

    response = window.run()
    if response == Gtk.ResponseType.OK:
        file_path = window.get_filename()
        window.destroy()

        return file_path
    else:
        window.destroy()
        return False


def gtk_folder_chooser(parent, title='', icon_path=None, default_folder=None):

    window = Gtk.FileChooserDialog(
        title,
        parent,
        Gtk.FileChooserAction.SELECT_FOLDER,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    if icon_path is not None:
        window.set_icon_from_file(icon_path)

    if default_folder is not None:
        window.set_current_folder(default_folder)

    response = window.run()
    if response == Gtk.ResponseType.OK:
        folder_path = window.get_filename()
        window.destroy()

        return folder_path
    else:
        window.destroy()
        return False


class GUI(Gtk.Window):

    def __init__(self):

        self._paths = Paths()

        # Glade
        #
        builder = Gtk.Builder()
        builder.add_from_file(self._paths.GLADE_FILE)
        builder.connect_signals(self)

        glade_object_names = (
            'window_root',
                'menubar',
                    'menuitem_profile',
                    'menuitem_options',
                        'checkbutton_autosave',
                        'checkbutton_profile_buttons',
                        'checkbutton_delete_warning',
                        'menuitem_off_areas',
                    'liststore_profiles',
                    'combobox_profiles',
                    'tempobutton',
                    'box_profile_buttons',
                'color_chooser_widget',
                'box_area_labels',
                'box_areas',                
                'label_user_message',
                'scrolledwindow_no_computer',
            'window_new_profile',
                'entry_new_profile',
                'button_new_profile_create',
            'window_about',
            'window_computer_data',
                'textbuffer_computer_data')

        for glade_object in glade_object_names:
            setattr(self, glade_object, builder.get_object(glade_object))

        """
            Add the accel groups
        """
        for _id, shorcut in (('imagemenuitem_apply_configuration', 'a'),
                            ('imagemenuitem_save', 's'),
                            ('imagemenuitem_delete', 'd'),
                            ('imagemenuitem_new', 'n'),
                            ('imagemenuitem_quit', 'q'),
                            ('button_lights_on', 'o'),
                            ('button_lights_off', 'f'),
                            ('imagemenuitem_export', 'e'),
                            ('imagemenuitem_import', 'i')):

            imagemenuitem_apply_configuration = builder.get_object(_id)
            accel_group = Gtk.AccelGroup()
            self.window_root.add_accel_group(accel_group)
            imagemenuitem_apply_configuration.add_accelerator('activate', 
                                                              accel_group, 
                                                              ord(shorcut), 
                                                              Gdk.ModifierType.CONTROL_MASK, 
                                                              Gtk.AccelFlags.VISIBLE)

        """
            Ask to the user if he wants to import its global configuration
            (this is a support for older versions of alienware-kbl)
        """
        if (not os.path.exists(self._paths.CONFIGURATION_PATH) and os.path.exists(self._paths.BACKUP_CONFIG)) or \
           (not os.path.exists(self._paths.PROFILES_PATH) and os.path.exists(self._paths.BACKUP_PROFILES)):

            self.window_root.hide()

            if gtk_dialog_question(self.window_root, TEXT_COPY_CONFIG, icon=self._paths.SMALL_ICON):
                from distutils.dir_util import copy_tree

                if not os.path.exists(os.path.dirname(self._paths.CONFIGURATION_PATH)):
                    print_warning('Adding the configuration {}'.format(self._paths.CONFIGURATION_PATH))
                    os.makedirs(os.path.dirname(self._paths.CONFIGURATION_PATH))

                if not os.path.exists(self._paths.PROFILES_PATH):
                    os.makedirs(self._paths.PROFILES_PATH)

                shutil.copyfile(self._paths.BACKUP_CONFIG, self._paths.CONFIGURATION_PATH)
                copy_tree(self._paths.BACKUP_PROFILES, self._paths.PROFILES_PATH)

            self.window_root.show()


        self.apply_configuration = False
        self.thread_zones = True
        self.queue_zones = []
        self.ccp = CCParser(self._paths.CONFIGURATION_PATH, 'GUI Configuration')

        #   Load a configuration
        #
        computer_name = AKBLConnection._command('get_computer_name')
        self.computer = getattr(Computer, computer_name)()
        
        Theme.LOAD_profiles(self.computer, self._paths.PROFILES_PATH)
        self.POPULATE_liststore_profiles()

        """
            Extra GUI initialization
        """

        computer_data = AKBLConnection._command('get_computer_info')

        self.textbuffer_computer_data.set_text(TEXT_COMPUTER_DATA.format(*computer_data[0:5]))

        # Add the areas to the  "menuitem_off_areas"
        #
        self.menu_turn_off_areas = Gtk.Menu()
        self.areas_description_dict = dict((area.description, area.name) for area in self.theme.get_areas())
        active_configuration_areas = self.ccp.get_str_defval('areas_to_keep_on', '').split('|')

        for description, area in sorted(self.areas_description_dict.items(), key=lambda x: x[0]):
            checkbox = Gtk.CheckMenuItem(label=description)

            if area in active_configuration_areas:
                checkbox.set_active(True)

            checkbox.connect('activate', self.on_checkbox_turnoff_areas_changed)

            self.menu_turn_off_areas.append(checkbox)

        self.menuitem_off_areas.set_submenu(self.menu_turn_off_areas)

        # Extra stuff
        #
        self.checkbutton_autosave.set_active(self.ccp.get_bool_defval('auto_save', True))
        self.checkbutton_profile_buttons.set_active(self.ccp.get_bool_defval('profile_buttons', False))
        self.checkbutton_delete_warning.set_active(self.ccp.get_bool_defval('delete_warning', True))

        self.POPULATE_box_areas()

        self.window_root.show_all()

        if not self.checkbutton_profile_buttons.get_active():
            self.box_profile_buttons.hide()

        self.scrolledwindow_no_computer.hide()

        # Start the zones thread !
        #
        threading.Thread(target=self.THREAD_zones).start()

    def POPULATE_box_areas(self):
        """
            This will add all the Areas and Zones to the graphical interphase.
        """
        
        # Empty the labels box
        for area_label in self.box_area_labels.get_children():
            self.box_area_labels.remove(area_label)
        
        # Empty the grid
        for box_area in self.box_areas.get_children():
            self.box_areas.remove(box_area)


        # Populate the labels box and the grid
        #
        for area in self.theme.get_areas():
            
            area_label = Gtk.Label()
            area_label.set_text(area.description)
            area_label.set_xalign(0)
            area_label.set_size_request(width=100, height=112.5)
            self.box_area_labels.pack_start(child=area_label, expand=False, fill=False, padding=0)
            self.box_area_labels.show_all()
            
            add_button_column = area.get_number_of_zones() - 1
            box_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            for column_index, zone in enumerate(area.get_zones()):

                zone_widget = ZoneWidget(area_name=area.name,
                                         left_color=zone.get_left_color(),
                                         right_color=zone.get_right_color(),
                                         mode=zone.get_mode(),
                                         column=column_index,
                                         colorchooser_widget=self.color_chooser_widget)

                box_area.pack_start(child=zone_widget, expand=False, fill=False, padding=5)

                if column_index == add_button_column:
                    add_button = Gtk.Button(label=TEXT_ADD)
                    add_button.set_alignment(0.5, 0.5)
                    add_button.connect('button-press-event', self.on_button_add_zone_clicked, area, box_area, column_index + 1)
                    box_area.pack_start(child=add_button, expand=False, fill=False, padding=5)

            self.box_areas.pack_start(child=box_area, expand=False, fill=False, padding=5)

        self.box_areas.show_all()

    def POPULATE_liststore_profiles(self):

        self.liststore_profiles.clear()

        for profile_name in sorted(Theme.AVAILABLE_THEMES.keys()):
            self.liststore_profiles.append([profile_name])

        row, _ = Theme.GET_last_configuration()

        self.combobox_profiles.set_active(row)

        self.speed = self.theme.get_speed()

    def DELETE_current_configuration(self):

        if self.checkbutton_delete_warning.get_active():
            Gdk.threads_enter()
            if not gtk_dialog_question(self.window_root, TEXT_CONFIRM_DELETE_CONFIGURATION, icon=self._paths.SMALL_ICON):
                Gdk.threads_leave()
                return
            Gdk.threads_leave()

        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_CONFIGURATION_DELETED)
        Gdk.threads_leave()

        Theme.AVAILABLE_THEMES.pop(self.theme.name)

        if os.path.exists(self.theme.path):
            os.remove(self.theme.path)

        if len(Theme.AVAILABLE_THEMES.keys()) == 0:
            Theme.CREATE_default_profile(self.computer)

        Gdk.threads_enter()
        self.POPULATE_liststore_profiles()
        Gdk.threads_leave()

        AKBLConnection._command('reload_configurations')

        sleep(0.5)

        Gdk.threads_enter()
        self.label_user_message.set_text(' ')
        Gdk.threads_leave()

    def THREAD_zones(self):
        """
            This thread scans the zones box in order to find color changes,
            mode changes or deletions.
        """
        self._light_changes = False

        while self.thread_zones:
            # Get the update of the zones and delete them if requested
            #
            for box_area in self.box_areas.get_children():
                deleted = False

                for selected_widget in box_area.get_children():

                    #
                    # Delete the zone from the GUI
                    #
                    if isinstance(selected_widget, ZoneWidget) and selected_widget.get_mode() == 'delete':

                        self._light_changes = True
                        deleted = True
                        area = self.theme.get_area_by_name(selected_widget.get_area_name())

                        column = selected_widget.get_column()

                        self.theme.delete_zone(selected_widget.get_area_name(), column)

                        after = False
                        for widget in box_area.get_children():
                            if widget == selected_widget:
                                after = True

                            if after and isinstance(widget, ZoneWidget):
                                
                                Gdk.threads_enter()
                                column = widget.get_column() # putting it here avoids a segmentation fault problem.
                                widget.set_column(column - 1)
                                Gdk.threads_leave()

                        Gdk.threads_enter()
                        box_area.remove(selected_widget)
                        Gdk.threads_leave()

                    elif deleted and self._light_changes and isinstance(selected_widget, Gtk.Button):
                        Gdk.threads_enter()
                        box_area.remove(selected_widget)
                        Gdk.threads_leave()

                        button = Gtk.Button(label=TEXT_ADD)
                        button.set_alignment(0.5, 0.5)
                        button.connect('button-press-event', self.on_button_add_zone_clicked, area, box_area, column)
                        box_area.pack_start(button, False, False, 5)

                    elif isinstance(selected_widget, ZoneWidget) and selected_widget.color_updated:
                        #
                        # Update the theme
                        #
                        self.theme.modify_zone(area_name=selected_widget.get_area_name(),
                                               column=selected_widget.get_column(),
                                               left_color=selected_widget.get_left_color(),
                                               right_color=selected_widget.get_right_color(),
                                               mode=selected_widget.get_mode())

                        selected_widget.color_updated = False
                        self._light_changes = True

            if self._light_changes:
                Gdk.threads_enter()
                self.box_areas.show_all()
                Gdk.threads_leave()

                if self.checkbutton_autosave.get_active():
                    threading.Thread(target=self.SAVE_configuration_file).start()
                
                self._light_changes = False

            sleep(0.1)

    def TURN_lights_off(self):

        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_SHUTTING_LIGHTS_OFF)
        Gdk.threads_leave()

        AKBLConnection._command('set_lights', False)

        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()

    def NEW_profile(self):
        text = self.entry_new_profile.get_text()

        self.window_new_profile.hide()

        clone = deepcopy(Theme.AVAILABLE_THEMES[self.theme.name])
        clone.name = text
        clone.path = '{}{}.cfg'.format(self._paths.PROFILES_PATH, text)
        clone.save()
        Theme.AVAILABLE_THEMES[clone.name] = clone
        self.POPULATE_liststore_profiles()

        AKBLConnection._command('reload_configurations')


    def ILUMINATE_keyboard(self):

        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_APPLYING_CONFIGURATION)
        Gdk.threads_leave()

        # This is to make the program recognize the last profile that has been
        # used
        try:
            # Patch (#12)
            os.utime(self.theme.path, None)
        except Exception:
            print_error('It was not possible to os.utime the profile path: \n{}\n{}'.format(self.theme.path), format_exc())

        AKBLConnection._command('reload_configurations')

        AKBLConnection.set_lights(True)

        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()

    def SAVE_configuration_file(self):

        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_SAVING_THE_CONFIGURATION)
        Gdk.threads_leave()

        self.theme.save()

        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()

    def on_imagemenuitem_computer_data_activate(self, button, data=None):
        self.window_computer_data.show()

    def on_button_computer_data_close_clicked(self, button, data=None):
        self.window_computer_data.hide()

    def on_checkbox_turnoff_areas_changed(self, checkbox, data=None):
        areas_to_keep_on=(self.areas_description_dict[checkbox.get_label()]
                                for checkbox in self.menu_turn_off_areas.get_children() if checkbox.get_active())
        
        self.ccp.write('areas_to_keep_on', '|'.join(areas_to_keep_on))

    def on_checkbutton_delete_warning_activate(self, button, data=None):
        self.ccp.write('delete_warning', self.checkbutton_delete_warning.get_active())

    def on_checkbutton_autosave_activate(self, button, data=None):
        self.ccp.write('auto_save', self.checkbutton_autosave.get_active())

    def on_checkbutton_profile_buttons_activate(self, button, data=None):
        if self.checkbutton_profile_buttons.get_active():
            self.box_profile_buttons.show()
            self.ccp.write('profile_buttons', True)
        else:
            self.box_profile_buttons.hide()
            self.ccp.write('profile_buttons', False)

    def on_button_about_activate(self, button, data=None):
        self.response = self.window_about.run()
        self.window_about.hide()

    def on_button_new_profile_cancel_clicked(self, button, data=None):
        self.window_new_profile.hide()

    def on_button_add_zone_clicked(self, button, event, area, area_box, column):
        """
            This button is not in glade, it is dynamically generated.
        """
        
        new_zone = ZoneWidget(area_name=area.name,
                              left_color=self.computer.DEFAULT_COLOR,
                              right_color=self.computer.DEFAULT_COLOR,
                              mode='fixed',
                              column=column,
                              colorchooser_widget=self.color_chooser_widget)

        #
        # Update the configuration
        #
        area.add_zone(new_zone)
        area_box.remove(button)

        #
        # Update the GUI
        #
        new_button = Gtk.Button(label=TEXT_ADD)
        new_button.connect('button-press-event', self.on_button_add_zone_clicked, area, area_box, column + 1)

        area_box.pack_start(child=new_zone, expand=False, fill=False, padding=5)
        area_box.pack_start(child=new_button, expand=False, fill=False, padding=5)

        self._light_changes = True


    def on_tempobutton_value_changed(self, widget, value):
        if value < 1:
            value = 1
        elif value > 255:
            value = 255

        value = 256 - value

        self.theme.set_speed(value)
        
        if self.checkbutton_autosave.get_active():
            threading.Thread(target=self.SAVE_configuration_file).start()

    def on_combobox_profiles_changed(self, widget, data=None):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            profile_name = model[tree_iter][0]
            self.theme = Theme.AVAILABLE_THEMES[profile_name]
            self.POPULATE_box_areas()

    def on_button_new_profile_create_clicked(self, button, data=None):
        self.NEW_profile()

    def on_imagemenuitem_apply_configuration_activate(
            self, widget=None, data=None):
        threading.Thread(target=self.ILUMINATE_keyboard).start()

    def on_imagemenuitem_save_activate(self, widget=None, data=None):
        threading.Thread(target=self.SAVE_configuration_file).start()

    def on_imagemenuitem_lights_on_activate(self, button, data=None):
        threading.Thread(target=self.ILUMINATE_keyboard).start()

    def on_imagemenuitem_lights_off_activate(self, widget):
        threading.Thread(target=self.TURN_lights_off).start()

    def on_imagemenuitem_quit_activate(self, widget, data=None):
        self.thread_zones = False
        Gtk.main_quit()

    def on_imagemenuitem_import_activate(self, widget=None, data=None):
        file_path = gtk_file_chooser(parent=self.window_root,
                                     title=TEXT_CHOOSE_A_THEME,
                                     icon_path=self._paths.SMALL_ICON,
                                     filters=(("AKBL theme", '*.cfg'),))

        if file_path:
            new_path = self._paths.PROFILES_PATH + os.path.basename(file_path)

            if os.path.exists(new_path) and not gtk_dialog_question(self.window_root, TEXT_THEME_ALREADY_EXISTS):
                return

            shutil.copy(file_path, new_path)
            Theme.LOAD_profile(self.computer, new_path)
            self.POPULATE_liststore_profiles()

    def on_imagemenuitem_export_activate(self, widget=None, data=None):
        folder_path = gtk_folder_chooser(parent=self.window_root, title=TEXT_CHOOSE_A_FOLDER_TO_EXPORT, icon_path=self._paths.SMALL_ICON)

        if folder_path:
            new_path = '{}/{}.cfg'.format(folder_path, self.theme.name)

            if os.path.exists(new_path) and not gtk_dialog_question(
                    self.window_root, TEXT_THEME_ALREADY_EXISTS):
                return

            shutil.copy(self.theme.path, new_path)

    def on_imagemenuitem_new_activate(self, widget=None, data=None):
        self.entry_new_profile.set_text('')
        self.window_new_profile.show()

    def on_imagemenuitem_delete_activate(self, widget=None, data=None):
        threading.Thread(target=self.DELETE_current_configuration).start()

    def on_window_root_destroy(self, data=None):
        self.thread_zones = False
        Gtk.main_quit()

    def on_button_apply_clicked(self, button, data=None):
        self.on_imagemenuitem_apply_configuration_activate()

    def on_button_export_clicked(self, button, data=None):
        self.on_imagemenuitem_export_activate()

    def on_button_import_clicked(self, button, data=None):
        self.on_imagemenuitem_import_activate()

    def on_button_save_clicked(self, button, data=None):
        self.on_imagemenuitem_save_activate()

    def on_button_delete_clicked(self, button, data=None):
        self.on_imagemenuitem_delete_activate()

    def on_button_new_clicked(self, button, data=None):
        self.on_imagemenuitem_new_activate()

    def on_entry_new_profile_changed(self, widget, data=None):

        text = self.entry_new_profile.get_text()

        # Check for invalid names
        #
        if text == '':
            self.button_new_profile_create.set_sensitive(False)
            return

        invalid_names = os.listdir(self._paths.PROFILES_PATH)
        for name in invalid_names:
            if name == text:
                self.button_new_profile_create.set_sensitive(False)
                return

            elif text == name[:-4]:
                self.button_new_profile_create.set_sensitive(False)
                return

        for name in Theme.AVAILABLE_THEMES.keys():
            if name == text:
                self.button_new_profile_create.set_sensitive(False)
                return

        self.button_new_profile_create.set_sensitive(True)

    def on_colorchooserwidget2_button_press_event(self, button, data=None):
        if self.color_chooser_widget.get_property('show-editor'):
            self.color_chooser_widget.set_property('show-editor', False)


AKBLConnection = Bindings()

def main():

    if not AKBLConnection.ping():
        print_error("Failed to start the GUI because the daemon is off.")
        exit(1)
        
    GObject.threads_init()
    Gdk.threads_init()

    _ = GUI()
    Gtk.main()
