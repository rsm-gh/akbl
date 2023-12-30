#!/usr/bin/python3
#

#  Copyright (C) 2015-2018 Rafael Senties Martinelli.
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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from AKBL.Addons.GUI.ZoneWidget import ZoneWidget
from AKBL.Addons.GUI.ColorChooserToolbar.ColorChooserToolbar import ColorChooserToolbar

class DialogWindow(Gtk.Window):

    def __init__(self):
        
        Gtk.Window.__init__(self, title="Dialog Example")
        
        self.set_size_request(width=900, height=600)
        box = Gtk.VBox()
        grid = Gtk.Grid()
        viewport = Gtk.Viewport()
        viewport.add(grid)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(viewport)
        
        self.color_chooser_toolbar = ColorChooserToolbar(self)
        self.color_chooser_toolbar.connect('colorlist-changed', self.on_toolbar_colorlist_changed)
        
        
        box.pack_start(child=self.color_chooser_toolbar, expand=False, fill=True, padding=10)
        box.pack_start(child=scrolled_window, expand=True, fill=True, padding=0)
        
        self.add(box)
        
        # Add the Zone objects to be tested
        #
        for row_index in range(2):
            fixed_zone = ZoneWidget(area_name='PB',
                                    left_color='#020202',
                                    right_color='#020202',
                                    mode='fixed',
                                    column=0,
                                    get_color_callback=self.color_chooser_toolbar.get_current_rgba)
            
            grid.attach(child=fixed_zone, left=0, top=row_index, width=1, height=1)
            
            blink_zone = ZoneWidget(area_name='',
                                    left_color='#020202',
                                    right_color='#020202',
                                    mode='blink',
                                    column=1,
                                    get_color_callback=self.color_chooser_toolbar.get_current_rgba)
            
            grid.add(blink_zone)
            
            morph_zone = ZoneWidget(area_name='',
                                    left_color='#020202',
                                    right_color='#020202',
                                    mode='morph',
                                    column=2,
                                    get_color_callback=self.color_chooser_toolbar.get_current_rgba)
            
            grid.add(morph_zone)
            
    @staticmethod
    def on_toolbar_colorlist_changed(_):
        print("The toolbar colorlist changed.")
            
            
# Launch the interface
#

win = DialogWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

    