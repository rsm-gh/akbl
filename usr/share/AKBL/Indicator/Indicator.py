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
import sys
import Pyro4
import subprocess
from time import sleep
from threading import Thread, current_thread

gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, GLib
from gi.repository import AyatanaAppIndicator3 as AppIndicator

from AKBL.texts import Texts
from AKBL.Bindings import Bindings
from AKBL.console import print_error, print_debug

_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
_PROJECT_DIR = os.path.dirname(_SCRIPT_DIR)
sys.path.insert(0, _PROJECT_DIR)

from common import IndicatorCodes


class ConnectIndicator:

    def __init__(self, white=False):
        self.__akbl = Bindings()
        self.__indicator = Indicator(self, self.__akbl, white)
        self.__pyro_daemon = Pyro4.Daemon()
        self.__uri = self.__pyro_daemon.register(self.__indicator)

        print_debug("URI={}".format(self.__uri))

        Thread(target=self.__pyro_thread).start()
        Thread(target=self.connect).start()

    def connect(self):
        # Todo: read the return status of connect_indicator
        sleep(0.5)
        return self.__akbl.connect_indicator(self.__uri)

    def shutdown(self):
        self.__pyro_daemon.shutdown()

    def __pyro_thread(self):
        self.__pyro_daemon.requestLoop()


class Indicator:

    def __init__(self, parent, akbl=None, white=False):

        self.__parent = parent

        if akbl is None:
            self.__akbl = Bindings()
        else:
            self.__akbl = akbl

        # Status variables for the loop
        #
        self.__current_code = None  # the first status shall be obtained by the daemon loop

        image_dir = os.path.join(os.path.join(_SCRIPT_DIR, "img"))

        if white:
            suffix = "-white"
        else:
            suffix = ""

        self.__icon_no_daemon = os.path.join(image_dir, 'icon-no-daemon{}.png'.format(suffix))
        self.__icon_lights_on = os.path.join(image_dir, 'icon-on{}.png'.format(suffix))
        self.__icon_lights_off = os.path.join(image_dir, 'icon-off{}.png'.format(suffix))

        # GUI stuff
        #
        self.__app_indicator = AppIndicator.Indicator.new_with_path(
            'akbl-indicator',
            self.__icon_no_daemon,
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

        #
        # Scan Thread
        #

        self.__thread_scan_daemon = Thread(target=self.__thread_daemon_check)
        self.__thread_scan_daemon.start()

    """
        Public & Pyro Methods
    """

    @Pyro4.expose
    def ping(self) -> None:
        print_debug()

    @Pyro4.expose
    def load_profiles(self,
                      profiles_name: list[str],
                      current_profile: str,
                      state: bool) -> None:

        print_debug("current_profile={}, state={}, profiles_name={}".format(current_profile,
                                                                            state,
                                                                            profiles_name))

        for children in self.__submenu_profiles.get_children():
            self.__submenu_profiles.remove(children)

        for profile_name in sorted(profiles_name):
            submenu = Gtk.CheckMenuItem(label=profile_name)

            if profile_name == current_profile and state:
                submenu.set_active(True)

            submenu.connect('toggled', self.set_profile, profile_name)
            self.__submenu_profiles.append(submenu)

        self.__submenu_profiles.show_all()

    @Pyro4.expose
    def set_code(self, indicator_code: int) -> None:

        print_debug("indicator_code={}".format(indicator_code))

        enable_gui = None

        match indicator_code:
            case self.__current_code:
                pass

            case IndicatorCodes.lights_on:

                if self.__current_code == IndicatorCodes.daemon_off:
                    enable_gui = True

                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_lights_on, Texts.Indicator.lights_on)

            case IndicatorCodes.lights_off:

                if self.__current_code == IndicatorCodes.daemon_off:
                    enable_gui = True

                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_lights_off, Texts.Indicator.lights_off)

            case IndicatorCodes.daemon_off:
                enable_gui = False
                self.__current_code = indicator_code
                self.__app_indicator.set_icon_full(self.__icon_no_daemon, Texts.Indicator.no_daemon)

            case _:
                print_error("wrong indicator code {}".format(indicator_code))

        if enable_gui is not None:
            self.__submenu_switch_state.set_sensitive(enable_gui)
            self.__profiles_menu.set_sensitive(enable_gui)

    @Pyro4.expose
    def set_profile(self, _widget: object, profile_name: str) -> None:
        print_debug("profile_name={}".format(profile_name))
        self.__akbl.set_profile(profile_name)

    """
        Private methods
    """

    def __thread_daemon_check(self):

        t = current_thread()
        while getattr(t, "do_run", True):

            if self.__akbl.ping():

                if self.__current_code == IndicatorCodes.daemon_off:
                    self.__parent.connect()
                    self.__akbl.update_indicator()

            elif self.__current_code != IndicatorCodes.daemon_off:
                GLib.idle_add(self.set_code, IndicatorCodes.daemon_off)

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
        self.__akbl.disconnect_indicator()

        if self.__parent is not None:
            self.__parent.shutdown()

        self.__thread_scan_daemon.do_run = False
        self.__thread_scan_daemon.join()

        Gtk.main_quit()

    @staticmethod
    def __on_menuitem_gui(*_):
        subprocess.run('akbl')


if __name__ == "__main__":
    white_icon = '--white' in sys.argv
    _ = ConnectIndicator(white_icon)
    Gtk.main()
