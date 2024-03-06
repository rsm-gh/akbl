#!/usr/bin/python3
#

#  Copyright (C) 2024 Rafael Senties Martinelli
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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from GUI.MainWindow import MainWindow


class AKBLApp(Gtk.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__gui = None

    def do_activate(self):
        active_window = self.props.active_window
        if active_window:
            active_window.present()
        else:
            self.__gui = MainWindow(application=self)
            self.__gui.present()


app = AKBLApp(application_id="com.senties-martinelli.AKBL")
app.run(sys.argv)
