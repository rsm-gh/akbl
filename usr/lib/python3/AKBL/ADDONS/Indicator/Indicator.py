#!/usr/bin/python3
#

#  Copyright (C) 2015-2016, 2018  Rafael Senties Martinelli 
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
from gi.repository import AppIndicator3 as appindicator

import os
import threading
import Pyro4
from time import sleep


from AKBL.utils import print_error
from AKBL.Bindings import Bindings
from AKBL.Configuration.Paths import Paths
from AKBL.texts import (TEXT_PROFILES, 
                        TEXT_START_THE_GUI, 
                        TEXT_SWICH_STATE, 
                        TEXT_EXIT)


def daemon_is_active():
    if AKBLConnection.ping():
        return True

    return False

class ConnectIndicator:

    def __init__(self):
        self.connected = False
        self.daemon = Pyro4.Daemon()
        self.uri = self.daemon.register(Indicator(self))
        threading.Thread(target=self.pycore_thread).start()
        threading.Thread(target=self.connect).start()

    def pycore_thread(self):
        self.daemon.requestLoop()

    def connect(self):
        sleep(0.5)
        self.connected = AKBLConnection._command('indicator_init', self.uri)


class Indicator:

    def __init__(self, self_main):
        self._ = self_main

        self.paths = Paths()

        # Status variables for the loop
        #
        self.current_code = None
        self.check_daemon = True

        # GUI stuff
        #
        self.indicator = appindicator.Indicator.new_with_path(
            'akbl-indicator',
            self.paths.INDICATOR_NO_DAEMON_ICON,
            appindicator.IndicatorCategory.APPLICATION_STATUS,
            os.path.dirname(os.path.realpath(__file__)))

        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        self.profiles_menu = Gtk.MenuItem(label=TEXT_PROFILES)
        self.menu.append(self.profiles_menu)
        self.submenu_profiles = Gtk.Menu()
        self.profiles_menu.set_submenu(self.submenu_profiles)

        item = Gtk.MenuItem(label=TEXT_START_THE_GUI)
        item.connect('activate', self.on_menuitem_gui)
        self.menu.append(item)

        self.switch_state = Gtk.MenuItem(label=TEXT_SWICH_STATE)
        self.switch_state.connect('activate', self.on_menuitem_change)
        self.menu.append(self.switch_state)

        item = Gtk.MenuItem(TEXT_EXIT)
        item.connect('activate', self.on_menuitem_exit)
        self.menu.append(item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        self.set_code(666)
        threading.Thread(target=self.daemon_check).start()

    @Pyro4.expose
    def ping(self):
        pass

    @Pyro4.expose
    def set_code(self, val):
        """
            Codes:

                100: Lights On
                150: Lights Off
                666: Daemon Off
        """

        try:
            val = int(val)
        except:
            print("AKBL-Indicator: Wrong code {}".format(val))
            return

        if val != self.current_code:
            self.current_code = val

            if val in (100, 150):
                if val == 100:
                    self.indicator.set_icon(self.paths.INDICATOR_ON_ICON )

                elif val == 150:
                    self.indicator.set_icon(self.paths.INDICATOR_OFF_ICON )

                for children in self.menu.get_children():
                    children.set_sensitive(True)

            elif val == 666:
                self.indicator.set_icon(self.paths.INDICATOR_NO_DAEMON_ICON)
                self.switch_state.set_sensitive(False)
                self.profiles_menu.set_sensitive(False)

    @Pyro4.expose
    def load_profiles(self, items, current, state):
        
        for children in self.submenu_profiles.get_children():
            self.submenu_profiles.remove(children)

        for item in sorted(items):
            submenu = Gtk.CheckMenuItem(label=item)

            if item == current and state:
                submenu.set_active(True)

            submenu.connect('toggled', self.set_profile, item)
            self.submenu_profiles.append(submenu)
           
        
        self.submenu_profiles.show_all()

    @Pyro4.expose
    def set_profile(self, widget, item):
        AKBLConnection.set_profile(item)

    def daemon_check(self):
        while self.check_daemon:

            if daemon_is_active():
                if self.current_code == 666:
                    self._.connect()
                    AKBLConnection._command('indicator_get_state')

            elif self.current_code != 666:
                GObject.idle_add(self.set_code, 666)

            sleep(1)

    def on_menuitem_off(self, widget, data=None):
        AKBLConnection.set_lights(False)

    def on_menuitem_on(self, widget, data=None):
        AKBLConnection.set_lights(True)

    def on_menuitem_gui(self, widget, data=None):
        os.system('''setsid setsid akbl''')

    def on_menuitem_change(self, widget, data=None):
        AKBLConnection.switch_lights()

    def on_menuitem_exit(self, widget, data=None):
        AKBLConnection._command('indicator_kill')
        self._.daemon.shutdown()
        self.check_daemon = False
        Gtk.main_quit()


AKBLConnection = Bindings()

def main():
    
    if not AKBLConnection.ping():
        print_error("Failed to start the Indicator because the daemon is off.")
        exit(1)    
    
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    GObject.threads_init()
    Gdk.threads_init()
    _ = ConnectIndicator()
    Gtk.main()
