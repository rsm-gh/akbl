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

import os
import sys
import shutil
from time import sleep
from gi.repository import Gtk, Gdk, GLib
from gi.repository.GdkPixbuf import Pixbuf
from threading import Thread, current_thread

from AKBL import settings
from AKBL.Texts import Texts
from AKBL.Paths import Paths
from AKBL.Bindings import Bindings
from AKBL.CCParser import CCParser
from AKBL.console_printer import print_warning
from AKBL.Computer.Computer import Computer
from AKBL.Theme import factory as theme_factory
import AKBL.Computer.factory as computer_factory

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.dirname(_SCRIPT_DIR))

from GUI.AreaItemWidget import AreaItemWidget
from GUI.ColorChooserToolbar.ColorChooserToolbar import ColorChooserToolbar
from gtk_utils import (gtk_dialog_question,
                       gtk_dialog_info,
                       gtk_file_chooser,
                       gtk_folder_chooser)


class MainWindow:

    def __init__(self, application):

        self.__application = application
        self.__bindings = Bindings(sender="GUI")
        self.__paths = Paths()
        self.__response = None

        # Glade
        #
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(_SCRIPT_DIR, "GUI.glade"))
        builder.connect_signals(self)

        glade_object_names = (
            'window_root',
            'menubar',
            'menuitem_profile',
            'menuitem_options',
            'checkbutton_autosave',
            'checkbutton_delete_warning',
            'menuitem_off_areas',
            'menuitem_apply_theme',
            'menuitem_lights_on',
            'menuitem_lights_off',
            'liststore_themes',
            'combobox_profiles',
            'tempobutton',
            'label_computer_model',
            'label_daemon_off',
            'box_profile_buttons',
            'horizontal_main_box',
            'box_area_labels',
            'box_areas',
            'window_new_profile',
            'entry_new_profile',
            'button_new_profile_create',
            'window_about')

        for glade_object in glade_object_names:
            setattr(self, glade_object, builder.get_object(glade_object))

        self.window_root.connect('delete-event', self.quit)
        self.window_root.set_application(self.__application)

        #
        #    Add the accel groups
        #
        for _id, shortcut in (('menuitem_apply_theme', 'a'),
                              ('menuitem_save', 's'),
                              ('menuitem_delete', 'd'),
                              ('menuitem_new', 'n'),
                              ('menuitem_quit', 'q'),
                              ('menuitem_lights_on', 'o'),
                              ('menuitem_lights_off', 'f'),
                              ('menuitem_export', 'e'),
                              ('menuitem_import', 'i')):
            menuitem_apply_theme = builder.get_object(_id)
            accel_group = Gtk.AccelGroup()
            self.window_root.add_accel_group(accel_group)
            menuitem_apply_theme.add_accelerator('activate',
                                                         accel_group,
                                                         ord(shortcut),
                                                         Gdk.ModifierType.CONTROL_MASK,
                                                         Gtk.AccelFlags.VISIBLE)

        self.__ccp = CCParser(self.__paths._configuration_file, 'GUI Configuration')

        #
        #
        self.__color_chooser_toolbar = ColorChooserToolbar(self)
        self.__color_chooser_toolbar.set_orientation(Gtk.Orientation.VERTICAL)
        self.__color_chooser_toolbar.connect("colorlist-changed", self.on_toolbar_colorlist_changed)
        default_toolbar_colors = self.__ccp.get_list('toolbar_colors')
        if len(default_toolbar_colors) > 0:
            self.__color_chooser_toolbar.set_colors(default_toolbar_colors)

        #   Load a configuration
        #
        self.__computer = computer_factory.get_default_computer()
        if self.__computer is None:  # todo: display message install computer model
            self.__computer = Computer()

        self.label_computer_model.set_text(self.__computer.name)

        theme_name = theme_factory.get_last_theme_name(self.__paths._themes_dir)
        if theme_name is None:
            self.__theme = theme_factory.create_default_theme(self.__computer, self.__paths._themes_dir)
        else:
            self.__theme = theme_factory.get_theme_by_name(self.__computer,
                                                           self.__paths._themes_dir,
                                                           theme_name)

        self.__populate_liststore_themes()

        #
        #    Extra GUI initialization
        #
        self.window_about.set_version(f"v{settings.__version__}")

        # Add the areas to the "menuitem_off_areas"
        #
        self.__menu_turn_off_areas = Gtk.Menu()
        self.__areas_description_dict = dict((area._description, area._name) for area in self.__theme.get_areas())

        active_configuration_areas = self.__ccp.get_str_defval('areas_to_keep_on', '').split('|')

        for description, area in sorted(self.__areas_description_dict.items(), key=lambda x: x[0]):
            checkbox = Gtk.CheckMenuItem(label=description)

            if area in active_configuration_areas:
                checkbox.set_active(True)

            checkbox.connect('activate', self.on_checkbox_turnoff_areas_changed)

            self.__menu_turn_off_areas.append(checkbox)

        self.menuitem_off_areas.set_submenu(self.__menu_turn_off_areas)

        # Extra stuff
        #
        self.horizontal_main_box.add(self.__color_chooser_toolbar)
        self.horizontal_main_box.reorder_child(self.__color_chooser_toolbar, 0)

        self.checkbutton_autosave.set_active(self.__ccp.get_bool_defval('auto_save', True))
        self.checkbutton_delete_warning.set_active(self.__ccp.get_bool_defval('delete_warning', True))

        self.__populate_box_areas()

        icon_pixbuf = Pixbuf.new_from_file(self.__paths._icon_file)
        self.window_root.set_icon(icon_pixbuf)
        self.window_root.show_all()
        self.window_root.maximize()
        self.label_daemon_off.hide()

        #
        # Start the thread to scan the Daemon
        #
        self.__thread_scan_daemon = Thread(target=self.__on_thread_scan_daemon)
        self.__thread_scan_daemon.start()

    def present(self):
        self.window_root.present()

    def quit(self, *_):
        self.__thread_scan_daemon.do_run = False
        self.__thread_scan_daemon.join()
        self.__application.quit()

    def on_toolbar_colorlist_changed(self, *_):
        hex_colors = self.__color_chooser_toolbar.get_hex_colors()
        self.__ccp.write("toolbar_colors", hex_colors)

    def on_tempobutton_value_changed(self, _, value):

        self.__theme.set_speed(255 - value)

        if self.checkbutton_autosave.get_active():
            Thread(target=self.__on_thread_save_theme).start()

    def on_combobox_profiles_changed(self, widget, *_):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            theme_name = model[tree_iter][0]
            self.__theme = theme_factory.get_theme_by_name(self.__computer,
                                                           self.__paths._themes_dir,
                                                           theme_name)

            self.tempobutton.set_value(self.__theme.get_speed())
            self.__populate_box_areas()

    def on_entry_new_profile_changed(self, *_):

        text = self.entry_new_profile.get_text()

        # Check for invalid names
        #
        if text == '':
            self.button_new_profile_create.set_sensitive(False)
            return

        invalid_names = os.listdir(self.__paths._themes_dir)
        for name in invalid_names:
            if name == text:
                self.button_new_profile_create.set_sensitive(False)
                return

            elif text == name[:-4]:
                self.button_new_profile_create.set_sensitive(False)
                return

        if text in theme_factory.get_theme_names(self.__paths._themes_dir):
            self.button_new_profile_create.set_sensitive(False)
            return

        self.button_new_profile_create.set_sensitive(True)

    def on_checkbox_turnoff_areas_changed(self, *_):
        areas_to_keep_on = (self.__areas_description_dict[checkbox.get_label()]
                            for checkbox in self.__menu_turn_off_areas.get_children() if checkbox.get_active())

        self.__ccp.write('areas_to_keep_on', '|'.join(areas_to_keep_on))

    def on_areaitemwidget_updated(self, areaitem_widget):

        self.__theme.modify_areaitem(area_name=areaitem_widget.get_area_name(),
                                     column=areaitem_widget.get_column(),
                                     left_color=areaitem_widget.get_left_color(),
                                     right_color=areaitem_widget.get_right_color(),
                                     mode=areaitem_widget.get_mode())

        if self.checkbutton_autosave.get_active():
            Thread(target=self.__on_thread_save_theme).start()

    def on_areaitemwidget_request_delete(self, areaitem_widget):

        self.__theme.delete_areaitem(areaitem_widget.get_area_name(), areaitem_widget.get_column())
        areaitem_widget.destroy()

        # Reset the column of all the areaitem_widgets. This could be
        # improved by being done to only 1 box area.
        for box_area in self.box_areas:
            column_counter = 0
            for widget in box_area.get_children():
                if isinstance(widget, AreaItemWidget):
                    widget.set_column(column_counter)
                    column_counter += 1

        #
        #
        if self.checkbutton_autosave.get_active():
            Thread(target=self.__on_thread_save_theme).start()

    def on_checkbutton_delete_warning_activate(self, *_):
        self.__ccp.write('delete_warning', self.checkbutton_delete_warning.get_active())

    def on_checkbutton_autosave_activate(self, *_):
        self.__ccp.write('auto_save', self.checkbutton_autosave.get_active())

    def on_menuitem_apply_theme_activate(self, *_):
        if not os.path.exists(self.__theme.get_path()):
            gtk_dialog_info(self, Texts.GUI._theme_must_saved.format(self.__theme.get_name()))
            return

        Thread(target=self.__on_thread_apply_theme).start()

    def on_menuitem_save_activate(self, *_):
        Thread(target=self.__on_thread_save_theme).start()

    def on_menuitem_lights_on_activate(self, *_):
        Thread(target=self.__on_thread_set_lights, args=[True]).start()

    def on_menuitem_lights_off_activate(self, *_):
        Thread(target=self.__on_thread_set_lights, args=[False]).start()

    def on_menuitem_quit_activate(self, *_):
        self.quit()

    def on_menuitem_import_activate(self, *_):
        file_path = gtk_file_chooser(parent=self.window_root,
                                     title=Texts.GUI._theme_choose,
                                     icon_path=self.__paths._icon_file,
                                     filters=(("AKBL theme", '*.cfg'),))

        if not file_path:
            return

        destination_path = self.__paths._themes_dir + os.path.basename(file_path)
        if os.path.exists(destination_path) and not gtk_dialog_question(self.window_root,
                                                                        Texts.GUI._theme_duplicate):
            return

        shutil.copy(file_path, destination_path)

        theme = theme_factory.load_theme_from_file(self.__computer, destination_path)
        self.__populate_liststore_themes(sel_theme_name=theme.get_name())

    def on_menuitem_export_activate(self, *_):
        folder_path = gtk_folder_chooser(parent=self.window_root,
                                         title=Texts.GUI._theme_choose_folder,
                                         icon_path=self.__paths._icon_file)

        if folder_path is not None:
            new_path = '{}/{}.cfg'.format(folder_path, self.__theme.get_name())

            if os.path.exists(new_path) and not gtk_dialog_question(self.window_root,
                                                                    Texts.GUI._theme_duplicate):
                return

            shutil.copy(self.__theme.get_path(), new_path)

    def on_menuitem_new_activate(self, *_):
        self.entry_new_profile.set_text('')
        self.window_new_profile.show()

    def on_menuitem_delete_activate(self, *_):
        if self.checkbutton_delete_warning.get_active() and \
                not gtk_dialog_question(self.window_root,
                                        Texts.GUI._theme_confirm_delete.format(self.__theme.get_name()),
                                        icon=self.__paths._icon_file):
            return

        Thread(target=self.__on_thread_delete_current_configuration).start()

    def on_button_new_profile_create_clicked(self, *_):
        self.window_new_profile.hide()
        new_path = f'{self.__paths._themes_dir}{self.entry_new_profile.get_text()}.cfg'
        new_theme = theme_factory.copy_theme(self.__theme, new_path)
        new_theme.save()

        self.__populate_liststore_themes(sel_theme_name=new_theme.get_name())
        self.__bindings.reload_themes()

    def on_button_reset_toolbar_colors_activate(self, *_):
        self.__color_chooser_toolbar.reset_colors()

    def on_button_about_activate(self, *_):
        self.__response = self.window_about.run()
        self.window_about.hide()

    def on_button_new_profile_cancel_clicked(self, *_):
        self.window_new_profile.hide()

    def on_button_add_item_clicked(self, button, _, area, area_box):
        """
            This button is not in glade, it is dynamically generated.
        """

        nb_of_areaitem_widgets = sum(1 for child in area_box.get_children() if isinstance(child, AreaItemWidget))

        if nb_of_areaitem_widgets >= area._max_commands:
            gtk_dialog_info(self.window_root,
                            Texts.GUI._maximum_zones.format(area._description))
            return

        areaitem_widget = AreaItemWidget(area_name=area._name,
                                         left_color=self.__color_chooser_toolbar.get_current_hex_color(),
                                         right_color=self.__color_chooser_toolbar.get_current_hex_color(),
                                         mode='fixed',
                                         column=nb_of_areaitem_widgets,
                                         get_color_callback=self.__color_chooser_toolbar.get_current_rgba)

        areaitem_widget.connect("updated", self.on_areaitemwidget_updated)
        areaitem_widget.connect("request-delete", self.on_areaitemwidget_request_delete)

        #
        # Update the configuration
        #
        area.add_item(areaitem_widget)

        #
        # Update the GUI
        #
        area_box.remove(button)
        area_box.pack_start(child=areaitem_widget, expand=False, fill=False, padding=5)
        area_box.pack_start(child=button, expand=False, fill=False, padding=5)

    def __populate_box_areas(self):
        """
            This will add all the Areas and AreaItems to the graphical interphase.
        """

        # Empty the label box
        for area_label in self.box_area_labels.get_children():
            self.box_area_labels.remove(area_label)

        # Empty the grid
        for box_area in self.box_areas.get_children():
            self.box_areas.remove(box_area)

        # Populate the label box and the grid
        #
        for area in self.__theme.get_areas():

            area_label = Gtk.Label()
            area_label.set_text(area._description)
            area_label.set_xalign(0)
            area_label.set_size_request(width=100, height=112)
            self.box_area_labels.pack_start(child=area_label, expand=False, fill=False, padding=0)
            self.box_area_labels.show_all()

            box_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

            for column_index, areaitem in enumerate(area.get_items()):

                areaitem_widget = AreaItemWidget(area_name=area._name,
                                                 left_color=areaitem.get_left_color(),
                                                 right_color=areaitem.get_right_color(),
                                                 mode=areaitem.get_mode(),
                                                 column=column_index,
                                                 get_color_callback=self.__color_chooser_toolbar.get_current_rgba)

                areaitem_widget.connect("updated", self.on_areaitemwidget_updated)
                areaitem_widget.connect("request-delete", self.on_areaitemwidget_request_delete)

                box_area.pack_start(child=areaitem_widget, expand=False, fill=False, padding=5)

                if column_index + 1 >= area._max_commands:
                    break

            if area._max_commands > 1:
                add_button = Gtk.Button(label=Texts.GUI._add)
                add_button.connect('button-press-event', self.on_button_add_item_clicked, area, box_area)
                box_area.pack_start(child=add_button, expand=False, fill=False, padding=5)

            self.box_areas.pack_start(child=box_area, expand=False, fill=False, padding=5)

        self.box_areas.show_all()

    def __populate_liststore_themes(self, sel_theme_name: str = None):

        self.liststore_themes.clear()

        theme_names = theme_factory.get_theme_names(self.__paths._themes_dir)

        if sel_theme_name is None:
            sel_theme_name = theme_factory.get_last_theme_name(self.__paths._themes_dir)

        active_row = 0
        for i, theme_name in enumerate(theme_names):
            self.liststore_themes.append([theme_name])
            if theme_name == sel_theme_name:
                active_row = i

        self.combobox_profiles.set_active(active_row)

    def __on_thread_scan_daemon(self):
        """
            The thread will be executed much faster than the ping to avoid
            lagging the GUI when using the close button.
        """

        akbl_status = None
        last_pinged = .8

        t = current_thread()
        while getattr(t, "do_run", True):
            sleep(.2)
            last_pinged += .2

            if last_pinged < 1:
                continue
            else:
                last_pinged = 0

            status = self.__bindings.ping()

            if akbl_status != status:
                akbl_status = status

                if status:
                    GLib.idle_add(self.label_daemon_off.hide)
                else:
                    GLib.idle_add(self.label_daemon_off.show)

                GLib.idle_add(self.menuitem_apply_theme.set_sensitive, akbl_status)
                GLib.idle_add(self.menuitem_lights_on.set_sensitive, akbl_status)
                GLib.idle_add(self.menuitem_lights_off.set_sensitive, akbl_status)

            if not status:
                self.__bindings.reload_address(verbose=False)

    def __on_thread_delete_current_configuration(self):

        if os.path.exists(self.__theme.get_path()):
            os.remove(self.__theme.get_path())

        if len(theme_factory.get_theme_names(self.__paths._themes_dir)) == 0:
            theme_factory.create_default_theme(self.__computer, self.__paths._themes_dir)

        GLib.idle_add(self.__populate_liststore_themes)
        self.__bindings.reload_themes()

    def __on_thread_apply_theme(self):
        self.__bindings.set_theme(self.__theme.get_name())

    def __on_thread_set_lights(self, status):
        self.__bindings.set_lights(status)

    def __on_thread_save_theme(self):
        self.__theme.save()
