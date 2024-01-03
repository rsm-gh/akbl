#!/usr/bin/python3
#

#  Copyright (C) 2015-2016, 2018, 2024 Rafael Senties Martinelli.
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
import gi
import Pyro4
import threading
from time import sleep
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, GObject, Gdk
from gi.repository import AyatanaAppIndicator3 as AppIndicator

from AKBL import texts
from AKBL.Bindings import Bindings

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class ConnectIndicator:

    def __init__(self):
        self.__akbl = Bindings()
        self.__indicator = Indicator(self, self.__akbl)
        self.__pyro_daemon = Pyro4.Daemon()
        self.__uri = self.__pyro_daemon.register(self.__indicator)

        threading.Thread(target=self.__pyro_thread).start()
        threading.Thread(target=self.connect).start()

    def connect(self):
        # Todo: read the return status of indicator_start
        sleep(0.5)
        return self.__akbl.indicator_start(self.__uri)

    def shutdown(self):
        self.__pyro_daemon.shutdown()

    def __pyro_thread(self):
        self.__pyro_daemon.requestLoop()


class Indicator:

    def __init__(self, parent, akbl=None):

        self.__parent = parent

        if akbl is None:
            self.__akbl = Bindings()
        else:
            self.__akbl = akbl

        # Status variables for the loop
        #
        self.__current_code = None
        self.__check_daemon = True

        # GUI stuff
        #
        self.__icon_on = os.path.join(_SCRIPT_DIR, 'icon-on.png')
        self.__icon_off = os.path.join(_SCRIPT_DIR, 'icon-off.png')
        self.__icon_no_daemon = os.path.join(_SCRIPT_DIR, 'icon-no-daemon.png')

        self.__app_indicator = AppIndicator.Indicator.new_with_path(
            'akbl-indicator',
            self.__icon_no_daemon,
            AppIndicator.IndicatorCategory.APPLICATION_STATUS,
            _SCRIPT_DIR)

        self.__app_indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.__menu = Gtk.Menu()

        self.__profiles_menu = Gtk.MenuItem(label=texts.TEXT_PROFILES)
        self.__menu.append(self.__profiles_menu)
        self.__submenu_profiles = Gtk.Menu()
        self.__profiles_menu.set_submenu(self.__submenu_profiles)

        item = Gtk.MenuItem(label=texts.TEXT_START_THE_GUI)
        item.connect('activate', self.__on_menuitem_gui)
        self.__menu.append(item)

        self.__submenu_switch_state = Gtk.MenuItem(label=texts.TEXT_SWITCH_STATE)
        self.__submenu_switch_state.connect('activate', self.__on_menuitem_change)
        self.__menu.append(self.__submenu_switch_state)

        item = Gtk.MenuItem(texts.TEXT_EXIT)
        item.connect('activate', self.__on_menuitem_exit)
        self.__menu.append(item)

        self.__menu.show_all()
        self.__app_indicator.set_menu(self.__menu)

        self.set_code(666)
        threading.Thread(target=self.__daemon_check).start()

    """
        Public & Pyro Methods
    """

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
        except Exception:
            print("AKBL-Indicator: Wrong code {}".format(val))
            return

        if val == self.__current_code:
            return

        self.__current_code = val

        if val in (100, 150):
            if val == 100:
                self.__app_indicator.set_icon(self.__icon_on)

            elif val == 150:
                self.__app_indicator.set_icon(self.__icon_off)

            for children in self.__menu.get_children():
                children.set_sensitive(True)

        elif val == 666:
            self.__app_indicator.set_icon(self.__icon_no_daemon)
            self.__submenu_switch_state.set_sensitive(False)
            self.__profiles_menu.set_sensitive(False)

    @Pyro4.expose
    def load_profiles(self, items, current, state):

        for children in self.__submenu_profiles.get_children():
            self.__submenu_profiles.remove(children)

        for item in sorted(items):
            submenu = Gtk.CheckMenuItem(label=item)

            if item == current and state:
                submenu.set_active(True)

            submenu.connect('toggled', self.set_profile, item)
            self.__submenu_profiles.append(submenu)

        self.__submenu_profiles.show_all()

    @Pyro4.expose
    def set_profile(self, _, item):
        self.__akbl.set_profile(item)

    """
        Private methods
    """

    def __daemon_check(self):

        while self.__check_daemon:

            if self.__akbl.ping():

                if self.__current_code == 666:
                    self.__parent.connect()
                    self.__akbl.indicator_get_state()

            elif self.__current_code != 666:
                GObject.idle_add(self.set_code, 666)

            else:
                self.__akbl.reload_address(False)

            sleep(1)

    def __on_menuitem_off(self, *_):
        self.__akbl.set_lights(False)

    def __on_menuitem_on(self, *_):
        self.__akbl.set_lights(True)

    def __on_menuitem_change(self, *_):
        self.__akbl.switch_lights()

    def __on_menuitem_exit(self, *_):
        self.__akbl.indicator_kill()
        self.__parent.pyro_shutdown()
        self.__check_daemon = False
        Gtk.main_quit()

    @staticmethod
    def __on_menuitem_gui(*_):
        os.system('''setsid setsid akbl''')

if __name__ == "__main__":
    GObject.threads_init()
    Gdk.threads_init()
    _ = ConnectIndicator()
    Gtk.main()
