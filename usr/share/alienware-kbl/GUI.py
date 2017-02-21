#!/usr/bin/python3
#

#  Copyright (C) 2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf

import threading
import shutil
import getpass
from traceback import format_exc
from time import time, sleep
from copy import deepcopy

# local imports
import Configuration
from Engine import *
from Texts import *
from ZoneWidget import *
from CCParser import CCParser
from Paths import Paths
from common import getuser

try:
    # This exception is used when pyro
    # is not installed.
    
    from AlienwareKBL import *
    AKBLConnection=AlienwareKBL()
    if AKBLConnection.ping():
        AKBL_DAEMON=True
        import Computers
    else:
        AKBL_DAEMON=False
        print("Runing without daemon.")
except:
    AKBL_DAEMON=False
    print("Runing without daemon.")


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))

def get_text_gtk_buffer(textbuffer):
    return textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),True)  

def gtk_append_text_to_buffer(textbuffer, text):
    textbuffer.set_text(get_text_gtk_buffer(textbuffer) + text)


def gtk_dialog_question(parent, text1, text2=None, icon=None):

    dialog=Gtk.MessageDialog(parent,
                            Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.QUESTION,
                            Gtk.ButtonsType.YES_NO,
                            text1)
                            
                            
    if icon is not None:
        dialog.set_icon_from_file(icon)
    
    if text2 is not None:
        dialog.format_secondary_text(text2)
    
    response=dialog.run()
    if response == Gtk.ResponseType.YES:
        dialog.hide()
        return True
        
    elif response == Gtk.ResponseType.NO:
        dialog.hide()
        return False

def gtk_dialog_info(parent, text1, text2=None, icon=None):

    dialog=Gtk.MessageDialog(parent,
                             Gtk.DialogFlags.MODAL,
                             Gtk.MessageType.INFO,
                             Gtk.ButtonsType.CLOSE,
                             text1)
    
    if icon is not None:
        dialog.set_icon_from_file(icon)
    
    if text2 is not None:
        dialog.format_secondary_text(text2)
    
    response=dialog.run()
    dialog.destroy()


def gtk_file_chooser(parent, title='', icon_path=None, default_folder=None, filters=[]):

    window=Gtk.FileChooserDialog(   title,
                                    parent,
                                    Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, 
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
        filter = Gtk.FileFilter()
        filter.set_name(filter_name)
        filter.add_pattern(filter_extension)
        window.add_filter(filter)

    response=window.run()
    if response == Gtk.ResponseType.OK:
        file_path=window.get_filename()
        window.destroy()
        
        return file_path
    else:
        window.destroy()
        return False


def gtk_folder_chooser(parent, title='', icon_path=None, default_folder=None):

    window=Gtk.FileChooserDialog(   title,
                                    parent,
                                    Gtk.FileChooserAction.SELECT_FOLDER,(Gtk.STOCK_CANCEL, 
                                                                         Gtk.ResponseType.CANCEL,
                                                                         Gtk.STOCK_OPEN, 
                                                                         Gtk.ResponseType.OK))



    if icon_path is not None:
        window.set_icon_from_file(icon_path)

    if default_folder is not None:
        window.set_current_folder(default_folder)
    
    response=window.run()
    if response == Gtk.ResponseType.OK:
        folder_path=window.get_filename()
        window.destroy()
        
        return folder_path
    else:
        window.destroy()
        return False
        




class GUI(Gtk.Window):
    
    def __init__(self):
        
        self._paths=Paths()
        
        # Glade
        #
        builder = Gtk.Builder()
        builder.add_from_file(self._paths.GLADE_FILE)
        builder.connect_signals(self)

        glade_objects=(
            'window_root', 
                'label_computername', 'label_user_message', 'button_new_profile_create', 'checkbutton_no_root', 'menuitem_off_zones', 
                'checkbutton_autosave', 'checkbutton_boot_off', 'checkbutton_profile_buttons', 'checkbutton_delete_warning', 
                'checkbutton_static_colorchooser','colorchooserdialog', 'colorchooserwidget2', 
                'box_zones', 'entry_new_profile', 'liststore_profiles', 'tempobutton', 'box_profile_buttons', 
                'scrolledwindow_no_computer', 'combobox_profiles', 'combobox_modes', 'liststore_modes', 'textbuffer_computer_data',
                'menubar', 'menuitem_profile', 'menuitem_options', 'imagemenuitem_block_testing',
                
            'window_about', 
            'window_new_profile', 
            'window_colorselection', 
            'window_computer_data', 

            'window_block_testing', 
                'grid_common_blocks', 'textbuffer_block_testing', 'label_block_hex_test', 'entry_block_testing', 'entry_id_vendor',
                'entry_id_product', 'togglebutton_find_device', 'box_block_testing', 'spinbutton_block_speed', 
                'viewport_common_block', 'button_update_common_blocks', 'button_block_make_test', 'checkbutton_auto_turn_off', 
                'checkbutton_hex_format_when_finding', 'combobox_default_blocks', 'colorbutton_1_block', 'colorbutton_2_block', 
                'combobox_block_modes',
        )
        
        for glade_object in glade_objects:
            setattr(self, glade_object, builder.get_object(glade_object))
        
        self.colorbutton_1_block.set_color(Gdk.Color(red=1, green=65535, blue=1))
        self.colorbutton_2_block.set_color(Gdk.Color(red=65535, green=1, blue=1))
        
        
        """
            Add the accel groups
        """
        for id, shorcut in (    ('imagemenuitem_apply_configuration','a'),
                                ('imagemenuitem_save','s'),
                                ('imagemenuitem_delete','d'),
                                ('imagemenuitem_new','n'),
                                ('imagemenuitem_quit','q'),
                                ('button_lights_on','o'),
                                ('button_lights_off','f'),
                                ('imagemenuitem_export','e'),
                                ('imagemenuitem_import','i')
                            ):
        
        
            imagemenuitem_apply_configuration=builder.get_object(id)
            accel_group = Gtk.AccelGroup()
            self.window_root.add_accel_group(accel_group)
            imagemenuitem_apply_configuration.add_accelerator(  'activate', 
                                                                accel_group, ord(shorcut), 
                                                                Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
            


        if getuser() != 'root':
            self.imagemenuitem_block_testing.set_sensitive(False)
            

        """
            Option "on boot.."
        """
        _global_ccp=CCParser(self._paths.GLOBAL_CONFIG,'Global alienware-kbl Configuration')

        if _global_ccp.get_str_defval('boot_user','root') != getuser():
            self.checkbutton_boot_off.set_sensitive(False)


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
                    print('Warning: Adding the configuration',self._paths.CONFIGURATION_PATH)
                    os.makedirs(os.path.dirname(self._paths.CONFIGURATION_PATH))
                
                if not os.path.exists(self._paths.PROFILES_PATH):
                    os.makedirs(self._paths.PROFILES_PATH)
                
                shutil.copyfile(self._paths.BACKUP_CONFIG, self._paths.CONFIGURATION_PATH)
                copy_tree(self._paths.BACKUP_PROFILES, self._paths.PROFILES_PATH)
                
                
                
            self.window_root.show()
                        
        """
            Program Variables / Diver / Controller
        """
        if getuser() == 'root':
            self.driver = Driver()
            self.testing_driver = Driver()
        
        if not AKBL_DAEMON and self.driver.not_found:
            self.label_computername.set_label('')
            self.colorchooserwidget2.hide()
            self.box_profile_buttons.hide()
            self.menuitem_profile.set_sensitive(False)
            self.menuitem_options.set_sensitive(False)
            self.combobox_profiles.set_sensitive(False)
            self.scrolledwindow_no_computer.show_all()
            
            # Try to get the keyboard data to append to the Computer Data window
            data_info=DATA_INFO
            try:
                lines=os.popen('''lsusb''').readlines()
                for line in lines:
                    if 'Alienware' in line: # this could bug if there is any other device called Alienware.
                        line=line.split(' ')
                        data_info=os.popen('''lsusb -D /dev/bus/usb/{}/{}'''.format(line[1], line[3][:-1])).read()
                        
            except Exception as e:
                data_info=DATA_INFO_ERROR+e
                
            self.textbuffer_computer_data.set_text(data_info)
        else:
            
            if getuser() == 'root':
                self.controller = Controller(self.driver)
                self.computer=self.driver.computer
            else:
                computer_name=AKBLConnection._command('get_computer_name')
                self.computer=getattr(Computers, computer_name)()
                
                
            self.apply_configuration=False
            self.thread_zones=True
            self.queue_zones=[]
            self.ccp=CCParser(self._paths.CONFIGURATION_PATH,'GUI Configuration')

            #   Load a configuration
            #
            Configuration.LOAD_profiles(self.computer, self._paths.PROFILES_PATH)
            self.POPULATE_liststore_profiles()
            
            """
                Extra GUI initialization
            """


            self.label_computername.set_label('{} - {}'.format(getuser(), self.computer.name))
            
            
            if getuser() == 'root':
                computer_data=(self.computer.name, self.driver.vendorId,self.driver.productId, self.driver.dev)
            else:
                computer_data=AKBLConnection._command('get_computer_info')
                

            self.textbuffer_computer_data.set_text(TEXT_COMPUTER_DATA.format(*computer_data[0:5]))
            

            # Add the zones to turn off to the  "menuitem_off_zones"
            #
            self.menu_turn_off_zones=Gtk.Menu()
            self.zones_and_descriptions_dict=dict((self.theme.area[zone].description, zone) for zone in self.theme.area.keys())
            active_configuration_zones=self.ccp.get_str_defval('zones_to_keep_alive','').split('|')
            
            for description, zone in sorted(self.zones_and_descriptions_dict.items(), key=lambda x: x[0]):            
                checkbox=Gtk.CheckMenuItem(label=description)
                
                if zone in active_configuration_zones:
                    checkbox.set_active(True)
                
                checkbox.connect('activate', self.on_checkbox_turnoff_zones_checked)
                
                self.menu_turn_off_zones.append(checkbox)

            self.menuitem_off_zones.set_submenu(self.menu_turn_off_zones)


            # Extra stuff
            #
            self.checkbutton_autosave.set_active(self.ccp.get_bool_defval('auto_save', True))
            self.checkbutton_profile_buttons.set_active(self.ccp.get_bool_defval('profile_buttons', False))
            self.checkbutton_delete_warning.set_active(self.ccp.get_bool_defval('delete_warning', True))
            self.checkbutton_static_colorchooser.set_active(self.ccp.get_bool_defval('static_chooser',False))
            
            self.POPULATE_zones()
            
            self.window_root.show_all()
            
            if not self.checkbutton_profile_buttons.get_active():
                self.box_profile_buttons.hide()
                
            if not self.checkbutton_static_colorchooser.get_active():
                self.colorchooserwidget2.hide()
                
            self.scrolledwindow_no_computer.hide()
            
            
            # check for systemctl
            #if self.ccp.get_bool_defval('systemd', True):
                #if not os.path.exists(self._paths.SYSTEMCTL_PATH):
                    #gtk_dialog_info(self.window_root, TEXT_SYSTEMD)
                    #self.ccp.write('systemd', False)
                
            
            # Start the zones thread !
            #
            threading.Thread(target=self.THREAD_zones).start()


    def get_zones_to_keep_alive(self):
        return [self.zones_and_descriptions_dict[checkbox.get_label()] \
                    for checkbox in self.menu_turn_off_zones.get_children() if checkbox.get_active()]

    
    def POPULATE_zones(self):
        
        # empty the grid
        #
        for children in self.box_zones.get_children():
            self.box_zones.remove(children)

        # organize the zones order
        #
        ordered_areas=sorted(self.theme.area.keys(), key=lambda x:self.theme.area[x].description)
        #set the power buttons at the top. This was disabled because the multiple power buttons were disabled #100
        #if 'PB' in ordered_areas:
        #    ordered_areas.insert(0, ordered_areas.pop(ordered_areas.index('PB')))


        # populate
        #
        for key in ordered_areas: # rows
            
            area=self.theme.area[key]
            lenght=len(area)
            box=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            
            if 'PB' in key and lenght < 1: # replaced 8 by 1 because of the power button #100
                while lenght < 1: # replaced 8 by 1 because of the power button #100
                    self.theme.add_zone(deepcopy(area[0]))
                    lenght=len(area)
                
            
            for column, zone_data in enumerate(area):
                
                if 'PB' in key and column >= 1: # 7 replaced by 0 #100
                    continue
                
                zone_widget=Zone(zone_data.color1, zone_data.color2, self.colorchooserdialog, zone_data, column, self.colorchooserwidget2)
                zone_widget.set_mode(zone_data.mode)
                
                box.pack_start(zone_widget, False, False, 5)
                
                if column == lenght-1 and zone_data.name != 'PB' and zone_data.name != 'PBE':
                    button=Gtk.Button(label=TEXT_ADD)
                    button.set_alignment(0.5, 0.5)
                    button.connect('button-press-event', self.on_button_add_zone_clicked, zone_data, box, column+1)
                    box.pack_start(button, False, False, 5)

                
                self.box_zones.pack_start(box, False, False, 5)

            self.box_zones.show_all()

    def POPULATE_liststore_profiles(self):
        
        self.liststore_profiles.clear()
        
        for profile_name in sorted(Configuration.profiles.keys()):
            self.liststore_profiles.append([profile_name])
            
        row, name = Configuration.GET_last_configuration()  
            
        self.combobox_profiles.set_active(row)

        self.speed=self.theme.speed


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
        
        Configuration.profiles.pop(self.theme.name)
        
        if os.path.exists(self.theme.path):
            os.remove(self.theme.path)
        
        if len(Configuration.profiles.keys()) == 0:
            Configuration.CREATE_default_profile(self.computer)
        
        Gdk.threads_enter() 
        self.POPULATE_liststore_profiles()
        Gdk.threads_leave()


        if AKBL_DAEMON:
            AKBLConnection._command('reload_configurations')

        
        sleep(0.5)
        
        Gdk.threads_enter()
        self.label_user_message.set_text(' ')
        Gdk.threads_leave()


    def THREAD_zones(self):
        """
            This thread scans the zones grid in order to find color changes,
            mode changes or deletions.
        """
        self.light_changes=False
        
        while self.thread_zones:
            #Get the update of the zones and delete them if requested
            #   
            for row_box in self.box_zones.get_children():
                deleted=False
                for chosen_widget in row_box.get_children():
                    
                    # Delete from the GUI
                    if isinstance(chosen_widget, Zone) and chosen_widget.mode == 'delete':
                        self.light_changes=True
                        deleted=True

                        zone=chosen_widget.zone
                        column=chosen_widget.column

                        self.theme.delete_zone(zone, column)
                        
                        after=False
                        for widget in row_box.get_children():
                            if widget == chosen_widget:
                                after=True
                            
                            if after and isinstance(widget, Zone):
                                Gdk.threads_enter()
                                column=widget.column
                                widget.set_column(column-1)
                                Gdk.threads_leave()
                                    
                        Gdk.threads_enter()
                        row_box.remove(chosen_widget)
                        Gdk.threads_leave()
                
                    elif deleted and self.light_changes and isinstance(chosen_widget, Gtk.Button):
                        Gdk.threads_enter()
                        row_box.remove(chosen_widget)
                        Gdk.threads_leave()
                        
                        button=Gtk.Button(label=TEXT_ADD)
                        button.set_alignment(0.5, 0.5)
                        button.connect('button-press-event', self.on_button_add_zone_clicked, zone, row_box, column)
                        row_box.pack_start(button, False, False, 5)
                        
                                
                    elif isinstance(chosen_widget, Zone) and chosen_widget.color_updated:
                        # Update the configuration
                        self.theme.modify_zone( chosen_widget.zone, 
                                                        chosen_widget.column, 
                                                        rgb_to_hex(chosen_widget.color1), 
                                                        rgb_to_hex(chosen_widget.color2),  
                                                        chosen_widget.mode)
                        
                        chosen_widget.color_updated=False
                        self.light_changes=True
                            
            
            if self.light_changes:
                Gdk.threads_enter()
                self.box_zones.show_all()
                Gdk.threads_leave()

                if self.checkbutton_autosave.get_active():
                    threading.Thread(target=self.SAVE_configuration_file).start()
                self.light_changes=False    


            sleep(0.1)    

    def TURN_lights_off(self):
        
        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_SHUTTING_LIGHTS_OFF)
        Gdk.threads_leave()
        
        
        if getuser() == 'root':
            
            for state in (True, False):
                
                keep_alive_zones=self.get_zones_to_keep_alive()
                
                if keep_alive_zones == []:
                    self.controller.Set_Loop_Conf(state, self.driver.computer.BLOCK_LOAD_ON_BOOT)
                    self.controller.Reset(self.computer.RESET_ALL_LIGHTS_OFF)
                else:
                    """
                        This hack, it will set black as color to all the lights that should be turned off
                    """
                    self.controller.Set_Loop_Conf(False, self.driver.computer.BLOCK_LOAD_ON_BOOT)
                    self.controller.Add_Speed_Conf(1)

                    for key in sorted(self.theme.area.keys()):
                        if not key in keep_alive_zones:
                            area=self.theme.area[key]
                            for zone in area:
                                self.controller.Add_Loop_Conf(zone.regionId, 'fixed', '#000000', '#000000')

                            self.controller.End_Loop_Conf()

                    self.controller.End_Transfert_Conf()
                    self.controller.Write_Conf()
                    
                
            if AKBL_DAEMON:
                AKBLConnection._command('modify_lights_state', False)
        else:
            AKBLConnection._command('set_lights', False)
            
            
        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()


    def NEW_profile(self):
        text=self.entry_new_profile.get_text()
        
        self.window_new_profile.hide()
        
        clone=deepcopy(Configuration.profiles[self.theme.name])
        clone.name=text 
        clone.path='{}{}.cfg'.format(self._paths.PROFILES_PATH, text)
        clone.save()
        Configuration.profiles[clone.name]=clone
        self.POPULATE_liststore_profiles()
        
        if AKBL_DAEMON:
            AKBLConnection._command('reload_configurations')


    def ILUMINATE_keyboard_block(self):

        zone_color1=self.colorbutton_1_block.get_color()
        zone_color1=rgb_to_hex([zone_color1.red/65535.0, zone_color1.green/65535.0, zone_color1.blue/65535.0])
        
        zone_color2=self.colorbutton_2_block.get_color()
        zone_color2=rgb_to_hex([zone_color2.red/65535.0, zone_color2.green/65535.0, zone_color2.blue/65535.0])
        
        zone_color2=zone_color1
        
        zone_block=int(self.entry_block_testing.get_text())
        
        speed=self.spinbutton_block_speed.get_value_as_int()

        index = self.combobox_block_modes.get_active()
        model = self.combobox_block_modes.get_model()
        zone_mode = model[index][0]
        zone_mode = zone_mode.lower()

        # Log the test
        gtk_append_text_to_buffer(self.textbuffer_block_testing,TEXT_BLOCK_TEST.format( zone_block,
                                                                                hex(zone_block),
                                                                                zone_mode,
                                                                                speed,
                                                                                zone_color1,
                                                                                zone_color2,
                                                                            ))

        #
        #   Test
        #
        #self.testing_controller.Reset()
        self.testing_controller.Set_Loop_Conf(False, self.testing_driver.computer.BLOCK_LOAD_ON_BOOT)
        self.testing_controller.Add_Speed_Conf(speed*256)
        self.testing_controller.Add_Loop_Conf( zone_block, zone_mode, zone_color1, zone_color2)
        self.testing_controller.End_Loop_Conf()
        self.testing_controller.End_Transfert_Conf()
        self.testing_controller.Write_Conf()


    def ILUMINATE_keyboard(self):
        
        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_APPLYING_CONFIGURATION)
        Gdk.threads_leave()

        # This is to make the program recognize the last profile that has been used
        try: # Patch (#12)
            os.utime(self.theme.path, None)
        except Exception as e:
            print('Warning: It was not possible to os.utime the profile path: \n{}'.format(self.theme.path))
            print(format_exc())

        if AKBL_DAEMON:
            AKBLConnection._command('reload_configurations')

        if getuser() != 'root':
            AKBLConnection.set_lights(True)
            
        else:
            if AKBL_DAEMON:
                AKBLConnection._command('modify_lights_state', True)


            self.controller.Set_Loop_Conf(False, self.driver.computer.BLOCK_LOAD_ON_BOOT)
            self.controller.Add_Speed_Conf(self.theme.speed)

            for key in sorted(self.theme.area.keys()):
                area=self.theme.area[key]
                for zone in area:
                    self.controller.Add_Loop_Conf(  zone.regionId,
                                                    zone.mode,
                                                    zone.color1,
                                                    zone.color2)

                self.controller.End_Loop_Conf()

            self.controller.End_Transfert_Conf()
            self.controller.Write_Conf()
                
                
        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()

    def SAVE_configuration_file(self):
        
        Gdk.threads_enter()
        self.label_user_message.set_text(TEXT_SAVING_THE_CONFIGURATION)
        Gdk.threads_leave()
        
        self.theme.save()
        
        sleep(0.5)
        
        Gdk.threads_enter()
        self.label_user_message.set_text('')
        Gdk.threads_leave()


    def on_imagemenuitem_computer_data_activate(self, button, data=None):
        self.window_computer_data.show()
        
    def on_button_computer_data_close_clicked(self, button, data=None):
        self.window_computer_data.hide()
    
    def on_checkbutton_static_colorchooser_activate(self, button, data=None):
        if self.checkbutton_static_colorchooser.get_active():
            self.colorchooserwidget2.show()
            self.ccp.write('static_chooser', True)
        else:
            self.colorchooserwidget2.hide()
            self.ccp.write('static_chooser', False)

    def on_checkbox_turnoff_zones_checked(self, checkbox, data=None):
        self.ccp.write('zones_to_keep_alive', '|'.join(self.get_zones_to_keep_alive()))
        
    def on_checkbutton_delete_warning_activate(self, button, data=None):
        self.ccp.write('delete_warning', self.checkbutton_delete_warning.get_active())
        
    def on_checkbutton_autosave_activate(self, button, data=None):
        self.ccp.write('auto_save', self.checkbutton_autosave.get_active())
    
    def on_checkbutton_boot_off_activate(self, button, data=None):
        self.ccp.write('boot', self.checkbutton_boot_off.get_active())

    def on_checkbutton_profile_buttons_activate(self, button, data=None):
        if self.checkbutton_profile_buttons.get_active():
            self.box_profile_buttons.show()
            self.ccp.write('profile_buttons', True)
        else:
            self.box_profile_buttons.hide()
            self.ccp.write('profile_buttons', False)
            
    def on_button_about_activate(self, button, data=None):
        self.response=self.window_about.run()
        self.window_about.hide()
        
    def on_button_new_profile_cancel_clicked(self, button, data=None):
        self.window_new_profile.hide()
        
    def on_button_add_zone_clicked(self, button, event, zone, box, column):
        """
            This button is not in glade, is dynamically generated
        """
        zone=deepcopy(zone)
        zone.color1=self.computer.default_color
        zone.color2=self.computer.default_color
        zone.mode='fixed'       
        
        new_zone=Zone(self.computer.default_color, self.computer.default_color, self.colorchooserdialog, zone, column, self.colorchooserwidget2)        
        self.theme.add_zone(zone)

        box.remove(button)
        
        new_button=Gtk.Button(label=TEXT_ADD)
        new_button.connect('button-press-event', self.on_button_add_zone_clicked, zone, box, column+1)

        box.pack_start(new_zone, False, False, 5)
        box.pack_start(new_button, False, False, 5)

        self.light_changes=True

    def on_tempobutton_value_changed(self, widget, value):
        if value < 1:
            value = 1
        elif value > 255:
            value = 255
            
        value = 256 - value

        self.theme.set_speed(value*256)
        
    def on_tempobutton_button_release_event(self, widget, data=None):
        if self.checkbutton_autosave.get_active():
            threading.Thread(target=self.SAVE_configuration_file).start()
            
        
    def on_combobox_profiles_changed(self, widget, data=None):
        tree_iter=widget.get_active_iter()
        if tree_iter != None:
            model=widget.get_model()
            profile_name=model[tree_iter][0]
            self.theme=Configuration.profiles[profile_name]
            self.POPULATE_zones()            
        
    def on_button_new_profile_create_clicked(self, button, data=None):
        self.NEW_profile()

    def on_imagemenuitem_apply_configuration_activate(self, widget=None, data=None):
        threading.Thread(target=self.ILUMINATE_keyboard).start()

    def on_imagemenuitem_save_activate(self, widget=None, data=None):
        threading.Thread(target=self.SAVE_configuration_file).start()
    
    def on_imagemenuitem_lights_on_activate(self, button, data=None):
        threading.Thread(target=self.ILUMINATE_keyboard).start()
    
    def on_imagemenuitem_lights_off_activate(self, widget):
        threading.Thread(target=self.TURN_lights_off).start()
    
    def on_imagemenuitem_quit_activate(self, widget, data=None):
        self.thread_zones=False
        Gtk.main_quit()

    def on_imagemenuitem_import_activate(self, widget=None, data=None):
        file_path=gtk_file_chooser( parent=self.window_root, 
                                    title=TEXT_CHOOSE_A_THEME, 
                                    icon_path=self._paths.SMALL_ICON, 
                                    filters=(("AKBL theme",'*.cfg'),),
                                    )
                                    
                                    
        if file_path:
            new_path=self._paths.PROFILES_PATH+os.path.basename(file_path)
            
            
            if os.path.exists(new_path) and not gtk_dialog_question(self.window_root, TEXT_THEME_ALREADY_EXISTS):
                return
            
            shutil.copy(file_path, new_path)
            Configuration.LOAD_profile(self.computer, new_path)
            self.POPULATE_liststore_profiles()
            
            
    def on_imagemenuitem_export_activate(self, widget=None, data=None):
        folder_path=gtk_folder_chooser( parent=self.window_root, 
                                        title=TEXT_CHOOSE_A_FOLDER_TO_EXPORT, 
                                        icon_path=self._paths.SMALL_ICON,
                                        )
        
        
        if folder_path:
            new_path='{}/{}.cfg'.format(folder_path, self.theme.name)
            
            if os.path.exists(new_path) and not gtk_dialog_question(self.window_root, TEXT_THEME_ALREADY_EXISTS):
                return
            
            shutil.copy(self.theme.path, new_path)
        

    def on_imagemenuitem_new_activate(self, widget=None, data=None):
        self.entry_new_profile.set_text('')
        self.window_new_profile.show()
    
    def on_imagemenuitem_delete_activate(self, widget=None, data=None):
        threading.Thread(target=self.DELETE_current_configuration).start()
    
    def on_window_root_destroy(self, data=None):
        self.thread_zones=False
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
        
        text=self.entry_new_profile.get_text()
        
        # Check for invalid names
        #
        if text=='':
            self.button_new_profile_create.set_sensitive(False)
            return
            
        invalid_names=os.listdir(self._paths.PROFILES_PATH)
        for name in invalid_names:
            if name == text:
                self.button_new_profile_create.set_sensitive(False)
                return
        
            elif text == name[:-4]:
                self.button_new_profile_create.set_sensitive(False)
                return
                
        for name in Configuration.profiles.keys():
            if name == text:
                self.button_new_profile_create.set_sensitive(False)
                return
                
        self.button_new_profile_create.set_sensitive(True)
        
    def on_colorchooserwidget2_button_press_event(self, button, data=None):
        if self.colorchooserwidget2.get_property('show-editor'):
            self.colorchooserwidget2.set_property('show-editor', False)
        
    """
        BLOCK TESTING
    """
     
        
    def on_imagemenuitem_block_testing_activate(self, button, data=None):
        #
        #   Try to fill the vendor and product id
        #
        text=get_text_gtk_buffer(self.textbuffer_computer_data)
        
        if 'Vendor ID' in text and 'Product ID:' in text:
            # When the computer was recognized by the program
            for line in text.split('\n'):
                if 'Vendor ID' in line:
                    line=line.split(':')
                    self.entry_id_vendor.set_text(line[1].strip())
                elif 'Product ID' in line:
                    line=line.split(':')
                    self.entry_id_product.set_text(line[1].strip())
            
            self.checkbutton_hex_format_when_finding.set_active(False)
            
        else:
            # When the computer is not yet supported
            
            if 'idVendor' and 'idProduct' in text:
                for line in text.split('\n'):
                    if 'idVendor' in line:
                        line=line.split()
                        self.entry_id_vendor.set_text(line[1])
                        
                    elif 'idProduct' in line:
                        line=line.split()
                        self.entry_id_product.set_text(line[1])
                

        self.window_block_testing.show()
        self.window_root.hide()
        
        
    def on_entry_block_testing_changed(self, entry, data=None):
        text=entry.get_text()
        try:
            value=int(text)
            
            if value < 0:
                self.label_block_hex_test.set_text('Non > 0')
                self.button_block_make_test.set_sensitive(False)
            else:
                self.label_block_hex_test.set_text(hex(value))
                self.button_block_make_test.set_sensitive(True)
        
        except:
            self.label_block_hex_test.set_text('Non Int')
            self.button_block_make_test.set_sensitive(False)

        
        
    def on_togglebutton_find_device_clicked(self, button, data=None):
        
        if self.togglebutton_find_device.get_active():
            
            if self.checkbutton_hex_format_when_finding.get_active():
                vendor=int(self.entry_id_vendor.get_text(), 16)
                product=int(self.entry_id_product.get_text(), 16)
            else:
                vendor=int(self.entry_id_vendor.get_text())
                product=int(self.entry_id_product.get_text())
                
    
            device=self.testing_driver.FindDevice(id_vendor=vendor, id_product=product)

            if device:
                self.testing_controller=Controller(self.testing_driver)
                
                for i in range(30):
                    method=self.grid_common_blocks.get_child_at(0, i).get_text()
                    value=getattr(self.testing_driver.computer, method)
                    
                    self.grid_common_blocks.get_child_at(2, i).set_text(hex(value))
                    
                    entry=Gtk.Entry()
                    entry.set_text(str(value))
        
                    self.grid_common_blocks.attach(entry, 1, i, 1, 1)
                
                
                self.grid_common_blocks.show_all()
                
                self.box_block_testing.set_sensitive(True)
                self.entry_id_vendor.set_sensitive(False)
                self.entry_id_product.set_sensitive(False)
                gtk_append_text_to_buffer(self.textbuffer_block_testing, TEXT_DEVICE_FOUND.format(vendor, product))
                
                self.combobox_default_blocks.set_active(0) 
                
            else:
                self.box_block_testing.set_sensitive(False)
                self.togglebutton_find_device.set_active(False)
                self.entry_id_vendor.set_sensitive(True)
                self.entry_id_product.set_sensitive(True)
                gtk_append_text_to_buffer(self.textbuffer_block_testing, TEXT_DEVICE_NOT_FOUND.format(vendor, product))
                
        else:
            self.box_block_testing.set_sensitive(False)
            self.entry_id_vendor.set_sensitive(True)
            self.entry_id_product.set_sensitive(True)
            
    def on_button_update_common_blocks_clicked(self, button, data=None):
        try:
            for i in range(30):
                text=self.grid_common_blocks.get_child_at(0, i).get_text()
                entry=self.grid_common_blocks.get_child_at(1, i)
                new_value=entry.get_text()
                old_value=getattr(self.testing_driver.computer, text)
                try:
                    old_value=int(old_value, 16)
                except:
                    pass
                
                
                # Verify the value of the entry
                #
                submit=True
                try:
                    new_value=int(new_value)
                except:
                    gtk_append_text_to_buffer(self.textbuffer_block_testing, TEXT_NON_INTEGER.format(text, new_value))
                    new_value=old_value
                    submit=False
                
                if submit:
                    if new_value != old_value:
                        setattr(self.testing_driver.computer, text, new_value)
                        gtk_append_text_to_buffer(self.textbuffer_block_testing, TEXT_VALUE_CHANGED.format(text, new_value, hex(new_value)))
                        self.grid_common_blocks.get_child_at(2, i).set_text(hex(int(new_value)))    
                else:               
                    entry.set_text(str(old_value))
        except Exception as e:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n'+format_exc()+'\n')
            
            
    def on_button_block_make_test_clicked(self, button, data=None):
        if self.checkbutton_auto_turn_off.get_active():
            self.on_button_block_testing_lights_off_clicked(button)
        
        try:
            self.ILUMINATE_keyboard_block()
        except Exception as e:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n'+format_exc()+'\n')


    def on_button_block_testing_lights_off_clicked(self, button, data=None):
        try:
            self.testing_controller.Reset(self.testing_driver.computer.RESET_ALL_LIGHTS_OFF)
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n'+TEXT_BLOCK_LIGHTS_OFF+'\n')
        except Exception as e:
            gtk_append_text_to_buffer(self.textbuffer_block_testing, '\n'+format_exc())


    def on_checkbutton_protect_common_blocks_clicked(self, checkbutton, data=None):
        if checkbutton.get_active():
            self.viewport_common_block.set_sensitive(False)
            self.button_update_common_blocks.set_sensitive(False)
        else:
            self.viewport_common_block.set_sensitive(True)
            self.button_update_common_blocks.set_sensitive(True)


    def on_combobox_default_blocks_changed(self, combobox, data=None):
        index = combobox.get_active()
        model = combobox.get_model()
        value = model[index][0]
        
        if value == -1:
            self.entry_block_testing.set_sensitive(True)
        else:
            self.entry_block_testing.set_sensitive(False)
            self.entry_block_testing.set_text(str(value))
        
        

    def on_button_close_block_testing_clicked(self, button, data=None):
        self.window_block_testing.hide()
        self.window_root.show()



if __name__ == '__main__':
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    if not AKBL_DAEMON and getuser() != 'root':
        print(TEXT_THE_GUI_NEEDS_ROOT)
    else:
        GObject.threads_init()
        Gdk.threads_init()
        
        gui = GUI()
        Gtk.main()

