#!/usr/bin/python3
#

#  Copyright (C) 2018, 2024 Rafael Senties Martinelli.
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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from gi.repository import GObject

from AKBL.utils import rgb_to_hex

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, PROJECT_DIR)

from GUI.ColorChooserToolbar.ColorToolItem import ColorToolItem

_DEFAULT_HEX_COLORS = ('#ff0000',
                       '#ff00ff',
                       '#0000ff',
                       '#00ffff',
                       '#ff0000',
                       '#ff8000',
                       '#ffff00',
                       '#40ff00',
                       '#000000',
                       '#ffffff')



        
        
class ColorChooserToolbar(Gtk.Toolbar):
    
    def __init__(self, window_parent):
        
        super().__init__()
        
        GObject.signal_new('colorlist-changed', 
                           self, 
                           GObject.SIGNAL_RUN_LAST, 
                           GObject.TYPE_NONE, 
                           ())
        
        self.__window_parent = window_parent
        self.__color_selector = Gtk.ColorSelectionDialog("Select a color", window_parent)
        self.__current_colortoolitem = None
        
        add_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_button.connect("clicked", self.__on_add_button_clicked)
        add_button.set_label(None)
        self.insert(add_button, 0)
        
        self.reset_colors()


    def __on_add_button_clicked(self, _):
        
        response = self.__color_selector.run()
        
        if response == Gtk.ResponseType.OK:
            gdk_color = self.__color_selector.get_color_selection().get_current_color()
            rgba_color = Gdk.RGBA.from_color(gdk_color)
            
            self.add_color_area(rgba_color)
            self.emit('colorlist-changed')
        
        
        self.__color_selector.hide()

    def __on_colortoolitem_picked(self, color_toolitem):
        
        for child in self.get_children():
            if isinstance(child, ColorToolItem):
                
                if child != color_toolitem:
                    child.set_picked(False)
                else:
                    child.set_picked(True)
                    self.__current_colortoolitem = child
    
    
    def __on_colortoolitem_destroy_request(self, color_toolitem):
        
        select_color = color_toolitem.get_picked()
        
        color_toolitem.destroy()
        
        if self.get_nb_of_colortoolitems() == 0:
            self.reset_colors()
            
        
        if select_color:
            color_tool_items = [child for child in self.get_children() if isinstance(child, ColorToolItem)]
            for color_tool_item in sorted(color_tool_items, key=lambda x: x.get_position(), reverse=True):
                color_tool_item.set_picked(True)
                break
        
        self.emit('colorlist-changed')
    
    def reset_colors(self):
        self.set_colors(_DEFAULT_HEX_COLORS)

    def get_nb_of_colortoolitems(self):
        return sum(1 for child in self.get_children() if isinstance(child, ColorToolItem))

    def get_hex_colors(self):
        
        hex_colors = []

        color_tool_items = [child for child in self.get_children() if isinstance(child, ColorToolItem)]

        for color_tool_item in sorted(color_tool_items, key=lambda x: x.get_position()):      
            rgba = color_tool_item.get_current_rgba()
            hex_color = rgb_to_hex((rgba.red*255, rgba.green*255, rgba.blue*255))
            hex_colors.append(hex_color)
                
        return hex_colors
    
    
    def get_current_hex_color(self):
        """
            :return: The current HEX color
        """
        
        rgba = self.__current_colortoolitem.get_current_rgba()
        hex_color = rgb_to_hex((rgba.red*255, rgba.green*255, rgba.blue*255))
        
        return hex_color


    def set_colors(self, hex_color_list):
        
        # Delete all the current colors
        for child in self.get_children():
            if isinstance(child, ColorToolItem):
                child.destroy()

        # Populate with new colors
        for hex_color in hex_color_list:
            self.add_color_area(hex_color)
            
        self.emit('colorlist-changed')
        self.show_all()
    
    def get_current_rgba(self):
        """
            :return: The current Gdk.RGBA
        """
        
        return self.__current_colortoolitem.get_current_rgba()


    def add_color_area(self, color):
        
        # Create the tool item
        tool_item = ColorToolItem(color, self.__window_parent, self.get_nb_of_colortoolitems())
        tool_item.connect("picked", self.__on_colortoolitem_picked)
        tool_item.connect("request-delete", self.__on_colortoolitem_destroy_request)
        self.insert(tool_item, 1)
        
        # Select it
        self.__on_colortoolitem_picked(tool_item)
        
        # display all the items
        tool_item.show_all()
        

    

        
        