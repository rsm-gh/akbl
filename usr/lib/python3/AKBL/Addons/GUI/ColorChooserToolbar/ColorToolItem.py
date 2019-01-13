#!/usr/bin/python3
#

#  Copyright (C) 2018  Rafael Senties Martinelli
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
from gi.repository import Gtk, Gdk
from gi.repository import GObject

_LEFT_CLICK_ID = 1
_RIGHT_CLICK_ID = 3


class ColorToolItem(Gtk.ToolItem):
    
    def __init__(self, start_color, window_parent=None, position=0):
        
        super().__init__()

        self.set_position(position)

        self.__picked = False

        self._rectangle_width = 50
        self._rectangle_height = 50
        
        self.__menu = Gtk.Menu()
        gtk_image = Gtk.Image()
        gtk_image.set_from_stock(Gtk.STOCK_DELETE, 1)
        self.__delete_menuitem = Gtk.ImageMenuItem('Delete')
        self.__delete_menuitem.set_image(gtk_image)
        self.__delete_menuitem.connect('activate', self.__on_delete_menuitem_clicked)
        
        self.__menu.append(self.__delete_menuitem)
        self.__menu.show_all()

        
        self.__color_selector = Gtk.ColorSelectionDialog("Select a color", window_parent)
        self.set_color(start_color)
        
        self.__drawing_area = Gtk.DrawingArea()
        self.__drawing_area.set_size_request(self._rectangle_width, self._rectangle_height)
        self.__drawing_area.connect('draw', self.__on_draw)
        self.__drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.__drawing_area.connect('button-press-event', self.__on_clicked)
        
        self.add(self.__drawing_area)
        
        
    def set_color(self, color):
        
        if isinstance(color, str):
            self.__current_color = Gdk.RGBA()
            self.__current_color.parse(color)
        else:
            self.__current_color = color
        
    def set_picked(self, status):
        self.__picked = status

    def set_position(self, column):
        self.__position = column
        
    def get_position(self):
        return self.__position

    def get_picked(self):
        return self.__picked

    def get_current_rgba(self):
        return self.__current_color
        
    def __on_draw(self, drawing_area, cr):
        
        cr.rectangle(0, 0, self._rectangle_width, self._rectangle_height)
        cr.set_source_rgb(self.__current_color.red, self.__current_color.green, self.__current_color.blue)
        cr.fill()
          
        if self.__picked:
            cr.set_font_size(40)
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(5, self._rectangle_height-5)
            cr.show_text("✓")
        
        drawing_area.queue_draw_area(0, 0, self._rectangle_width, self._rectangle_height)
        
        return True
        
        
    def __on_clicked(self, widget, event):
        
        if event.button == _LEFT_CLICK_ID:
            
            if event.type == Gdk.EventType.BUTTON_PRESS:
                self.emit('picked')

            elif event.type == Gdk.EventType._2BUTTON_PRESS:
                response = self.__color_selector.run()
                
                if response == Gtk.ResponseType.OK:
                    gdk_color = self.__color_selector.get_color_selection().get_current_color()
                    rgba_color = Gdk.RGBA.from_color(gdk_color)
                    self.set_color(rgba_color)
                    self.emit('color-changed')
                    self.emit('picked')
                   
                self.__color_selector.hide()
                
                
        elif _RIGHT_CLICK_ID:
            self.__menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())

    def __on_delete_menuitem_clicked(self, widget):
        self.emit("request-delete")
        
# I ignore why this wasn't possible to be defined at __init__ as same as the ColorChooserToolbar 
GObject.type_register(ColorToolItem)
GObject.signal_new('color-changed', ColorToolItem, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())

GObject.type_register(ColorToolItem)
GObject.signal_new('picked', ColorToolItem, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())

GObject.type_register(ColorToolItem)
GObject.signal_new('request-delete', ColorToolItem, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
        