#!/usr/bin/python3
#

#  Copyright (C) 2015-2025 Rafael Senties Martinelli.
#
#  AKBL is free software; you can redistribute it and/or modify
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
import sys
import subprocess
from time import sleep
from threading import Thread, current_thread

try:
    from Pyro5.server import expose as pyro_server_expose
    from Pyro5.server import Daemon as PyroServerDaemon
except ImportError:
    from Pyro4 import expose as pyro_server_expose
    from Pyro4 import Daemon as PyroServerDaemon

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AyatanaAppIndicator3 as AppIndicator

from AKBL.Paths import Paths
from AKBL.Texts import Texts
from AKBL.Bindings import Bindings
from AKBL.settings import IndicatorCodes
from AKBL.Theme import factory
from AKBL.console_printer import print_error, print_debug

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_PROJECT_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _PROJECT_DIR)


class Indicator:

    def __init__(self, white=False):

        self.__paths = Paths()
        self.__current_code = -1

        if white:
            suffix = "-white"
        else:
            suffix = ""
        image_dir = os.path.join(os.path.join(_SCRIPT_DIR, "img"))
        self.__icon_no_daemon = os.path.join(image_dir, 'icon-no-daemon{}.png'.format(suffix))
        self.__icon_lights_on = os.path.join(image_dir, 'icon-on{}.png'.format(suffix))
        self.__icon_lights_off = os.path.join(image_dir, 'icon-off{}.png'.format(suffix))

        # GUI / Indicator
        #
        self.__app_indicator = AppIndicator.Indicator.new_with_path(
            'akbl-indicator',
            self.__icon_lights_off,
            AppIndicator.IndicatorCategory.APPLICATION_STATUS,
            image_dir)

        self.__app_indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        self.__menu = Gtk.Menu()

        item = Gtk.MenuItem(label=Texts.Indicator.start_gui)
        item.connect('activate', self.__on_menuitem_gui)
        self.__menu.append(item)

        self.__profiles_menu = Gtk.MenuItem(label=Texts.Indicator.profiles)
        self.__menu.append(self.__profiles_menu)
        self.__submenu_profiles = Gtk.Menu()
        self.__profiles_menu.set_submenu(self.__submenu_profiles)

        self.__submenu_switch_state = Gtk.MenuItem(label=Texts.Indicator.switch_state)
        self.__submenu_switch_state.connect('activate', self.__on_menuitem_change)
        self.__menu.append(self.__submenu_switch_state)

        item = Gtk.MenuItem(label=Texts.Indicator.exit)
        item.connect('activate', self.__on_menuitem_exit)
        self.__menu.append(item)

        self.__menu.show_all()
        self.__app_indicator.set_menu(self.__menu)

        # Pyro
        #
        self.__pyro_daemon = PyroServerDaemon()
        self.__uri = self.__pyro_daemon.register(self)
        print_debug("URI={}".format(self.__uri))
        Thread(target=self.__on_thread_pyro_loop).start()

        # AKBL Bindings
        self.__bindings = Bindings(sender="Indicator")
        self.__bindings.connect_indicator(self.__uri)

        #
        # Scan Thread
        #
        self.__thread_scan_daemon = Thread(target=self.__on_thread_scan_daemon)
        self.__thread_scan_daemon.start()

    """
        Public & Pyro Methods
    """
    @pyro_server_expose
    def ping(self) -> None:
        print_debug()

    @pyro_server_expose
    def exit(self, from_daemon: bool = True) -> None:

        if from_daemon:
            print_debug("Closing the indicator, requested by the daemon.")
        else:
            self.__bindings.disconnect_indicator()

        self.__pyro_daemon.shutdown()
        self.__thread_scan_daemon.do_run = False
        self.__thread_scan_daemon.join()

        Gtk.main_quit()

    @pyro_server_expose
    def load_themes(self,
                    current_profile: str,
                    state: bool) -> None:

        print_debug(f"current_profile={current_profile}, state={state}")

        for children in self.__submenu_profiles.get_children():
            self.__submenu_profiles.remove(children)

        for theme_name in factory.get_theme_names(self.__paths._themes_dir):
            submenu = Gtk.CheckMenuItem(label=theme_name)
            submenu.set_active(theme_name == current_profile and state)

            submenu.connect('toggled', self.set_theme, theme_name)
            self.__submenu_profiles.append(submenu)

        self.__submenu_profiles.show_all()

    @pyro_server_expose
    def set_code(self, indicator_code: int) -> None:

        print_debug("indicator_code={}".format(indicator_code))

        enable_gui = None
        children_state = None

        match indicator_code:
            case self.__current_code:
                print_debug("Exit", direct_output=True)

            case IndicatorCodes._lights_on:
                print_debug("Lights on", direct_output=True)

                if self.__current_code == IndicatorCodes._daemon_off:
                    enable_gui = True

                children_state = True
                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_lights_on, Texts.Indicator.lights_on)

            case IndicatorCodes._lights_off:
                print_debug("Lights Off", direct_output=True)

                if self.__current_code == IndicatorCodes._daemon_off:
                    enable_gui = True

                children_state = False
                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_lights_off, Texts.Indicator.lights_off)

            case IndicatorCodes._daemon_off:
                print_debug("Daemon off", direct_output=True)

                enable_gui = False
                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_no_daemon, Texts.Indicator.no_daemon)

            case _:
                print_error("wrong indicator code {}".format(indicator_code))

        if enable_gui is not None:
            self.__submenu_switch_state.set_sensitive(enable_gui)
            self.__profiles_menu.set_sensitive(enable_gui)

        if not children_state:
            for children in self.__submenu_profiles.get_children():
                children.set_active(children_state)

    @pyro_server_expose
    def set_theme(self, _widget: object, theme_name: str) -> None:
        print_debug("theme_name={}".format(theme_name))
        self.__bindings.set_theme(theme_name)

    """
        Private methods
    """

    def __on_thread_pyro_loop(self):
        self.__pyro_daemon.requestLoop()

    def __on_thread_scan_daemon(self):

        t = current_thread()
        while getattr(t, "do_run", True):

            if self.__bindings.ping():

                if self.__current_code in (IndicatorCodes._daemon_off, -1):
                    self.__bindings.connect_indicator(self.__uri)

            elif self.__current_code != IndicatorCodes._daemon_off:
                GLib.idle_add(self.set_code, IndicatorCodes._daemon_off)

            else:
                self.__bindings.reload_address(verbose=False)

            sleep(1)

    def __on_menuitem_off(self, *_):
        self.__bindings.set_lights(False)

    def __on_menuitem_on(self, *_):
        self.__bindings.set_lights(True)

    def __on_menuitem_change(self, *_):
        self.__bindings.switch_lights()

    def __on_menuitem_exit(self, *_):
        self.exit(from_daemon=False)

    @staticmethod
    def __on_menuitem_gui(*_):
        subprocess.run('akbl')


if __name__ == "__main__":
    _ = Indicator(white='--white' in sys.argv)
    Gtk.main()
