#!/usr/bin/python3
#

#  Copyright (C) 2015-2018  Rafael Senties Martinelli
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
import cairo


from AKBL.utils import print_warning
from AKBL.Paths import Paths

_IMAGES_PATH = Paths()._images_dir
_LEFT_CLICK_ID = 1
_RIGHT_CLICK_ID = 3

_BUTTONS_IMAGE_PATTERN = ['empty',
                          'fixed_on',
                          'morph_on',
                          'blink_on',
                          'empty',
                          'fixed_off',
                          'morph_off',
                          'blink_off']

_BUTTONS_IMAGE_PATTERN_WITH_DELETE = ['cross_on',
                                      'fixed_on',
                                      'morph_on',
                                      'blink_on',
                                      'cross_off',
                                      'fixed_off',
                                      'morph_off',
                                      'blink_off']


class ZoneWidget(Gtk.Frame):

    """
        Zone Widget Architecture:

            Gtk.Frame()
                > Gtk.Box()
                    > Gtk.DrawingArea()
                    > Gtk.DrawingArea()
                    > Gtk.VBox()
                        > Gtk.EventBox()
                            > Gtk.Image()
                        > Gtk.EventBox()
                            > Gtk.Image()
                        > Gtk.EventBox()
                            > Gtk.Image()
                        > Gtk.EventBox()
                            > Gtk.Image()
    """

    __gtype_name__ = 'ZoneWidget'

    def __init__(self, 
                 area_name, 
                 left_color, 
                 right_color,
                 mode, 
                 column, 
                 get_color_callback, 
                 hex_id=1):

        super().__init__()

        # Variables
        #
        self.__left_color = []
        self.__right_color = []
        self.__mode = ''
        
        self.__hex_id = ''
        self.__area_name = ''

        self._heigth = 100
        self._width = 90
        
        self.__command_buttons_events = []
        self.__command_buttons_state = [False,  # Delete button
                                        True,   # Fixed button
                                        False,  # Morph button
                                        False]  # Blink button



        # requested objects and variables
        #
        self.__get_color_callback = get_color_callback
        self.zone = None

        self.set_left_color(left_color)
        self.set_right_color(right_color)

        self.__commands_buttons_box = Gtk.VBox()

        # Create the Gtk objects
        #
        box = Gtk.Box()
        box.set_size_request(-1, -1)

        self.__left_drawing_area = Gtk.DrawingArea()
        self.__right_drawing_area = Gtk.DrawingArea()

        self.__left_drawing_area.set_size_request(self._width, self._heigth)
        self.__right_drawing_area.set_size_request(self._width, self._heigth)

        self.__left_drawing_area.connect('draw', self.__on_draw_drawingarea, 1)
        self.__right_drawing_area.connect('draw', self.__on_draw_drawingarea, 2)

        self.__left_drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.__right_drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self.__left_drawing_area.connect('button-press-event', self.__on_drawingarea_click, 1)
        self.__right_drawing_area.connect('button-press-event', self.__on_drawingarea_click, 2)

        # Finish the GTK interface
        #
        box.pack_start(child=self.__left_drawing_area, expand=False, fill=False, padding=0)
        box.pack_start(child=self.__right_drawing_area, expand=False, fill=False, padding=0)
        box.pack_start(child=self.__commands_buttons_box, expand=False, fill=False, padding=0)
        self.add(box)
        self.show_all()
        
        # Extra initialization
        #
        self.set_column(column)
        self.set_mode(mode)
        self.set_area_name(area_name)
        self.set_hex_id(hex_id)
        
    def __init_commands_box(self):
        
        # Remove the previous content
        for children in self.__commands_buttons_box.get_children():
            self.__commands_buttons_box.remove(children)
        self.__command_buttons_events = []
        
        # Populate
        for i in (4, 1, 6, 7):
            event_box = Gtk.EventBox()
            event_box.add(self.__get_command_button_image(i))

            if i == 4 and self.__column <= 0:
                pass
            else:
                event_box.connect('button-press-event', self.__on_command_button_click)

            self.__commands_buttons_box.pack_start(event_box, False, False, 0)
            self.__command_buttons_events.append(event_box)

        self.__update_command_buttons_background()
        self.__commands_buttons_box.show_all()

    def __on_drawingarea_click(self, widget, event, area_number):

        if event.button == _LEFT_CLICK_ID:

            color = self.__get_color_callback()

            if not color is None:

                if area_number == 1 or not self.__command_buttons_state[2]:  # morph
                    self.__left_color = color
                else:
                    self.__right_color = color

                self.emit('updated')

        self.__update_command_buttons_background()

    def __on_command_button_click(self, widget, data=None):
        
        old_mode = self.__mode

        for i in range(4):
            # Remove the buttons
            event_box = self.__command_buttons_events[i]
            event_box.remove(event_box.get_children()[0])

            # Populate with new images
            if event_box == widget:
                event_box.add(self.__get_command_button_image(i))
                self.__command_buttons_state[i] = True

                if i == 0:
                    self.__mode = 'delete'
                elif i == 1:
                    self.__mode = 'fixed'
                elif i == 2:
                    self.__mode = 'morph'
                elif i == 3:
                    self.__mode = 'blink'

                if self.__mode != old_mode and self.__mode != 'delete':
                    self.emit('updated')

            else:
                event_box.add(self.__get_command_button_image(i + 4))
                self.__command_buttons_state[i] = False

        self.__update_command_buttons_background()
        self.__commands_buttons_box.show_all()

        if self.__mode == 'delete':
            self.emit('request-delete')


    def __get_command_button_image(self, index):

        if self.__column == 0 or self.__area_name in ('PB','PBE'):
            return Gtk.Image.new_from_file('{}{}.png'.format(_IMAGES_PATH, _BUTTONS_IMAGE_PATTERN[index]))

        return Gtk.Image.new_from_file('{}{}.png'.format(_IMAGES_PATH, _BUTTONS_IMAGE_PATTERN_WITH_DELETE[index]))

    def __on_draw_drawingarea(self, widget, cr, area_number):

        if self.__command_buttons_state[2]:  # morph
            
            middle_color=self.middle_rgb_color((self.__left_color.red, self.__left_color.green, self.__left_color.blue),
                                          (self.__right_color.red, self.__right_color.green, self.__right_color.blue))
            
            middle_color = Gdk.RGBA(*middle_color)
            
            if area_number == 1:
                start_color = self.__left_color
                end_color = middle_color
            if area_number == 2:
                start_color = middle_color
                end_color = self.__right_color
        else:
            start_color = self.__left_color
            end_color =  self.__left_color
            self.__update_command_buttons_background()


        lg1 = cairo.LinearGradient(0.0, 0.0, self._width, 0)
        lg1.add_color_stop_rgb(0, start_color.red, start_color.green, start_color.blue)
        lg1.add_color_stop_rgb(1, end_color.red, end_color.green, end_color.blue)
        cr.rectangle(0, 0, self._width, self._heigth)
        cr.set_source(lg1)
        cr.fill()
        widget.queue_draw_area(0, 0, self._width, self._heigth)

        return True

    def __update_command_buttons_background(self):

        if self.__command_buttons_state[2]:  # morph
            gdk_color = self.__right_color
        else:
            gdk_color = self.__left_color

        for children in self.__commands_buttons_box.get_children():
            for child in children.get_children():
                child.override_background_color(Gtk.StateType.NORMAL, gdk_color)

        self.__commands_buttons_box.override_background_color(Gtk.StateType.NORMAL, gdk_color)

    def middle_rgb_color(self, rgb_color1, rgb_color2):
        """
            Return the middle RGB from two RGB colors.
            Useful for creating gradients !
        """
        return [((rgb_color1[0] + rgb_color2[0]) / 2.0),
                ((rgb_color1[1] + rgb_color2[1]) / 2.0),
                ((rgb_color1[2] + rgb_color2[2]) / 2.0)]

    def set_hex_id(self, hex_id):
        self.__hex_id = hex_id

    def set_area_name(self, area_name):
        self.__area_name = area_name

    def set_column(self, column):
        self.__column = column
        self.__init_commands_box()

    def set_mode(self, mode):

        if mode == 'fixed':
            self.__mode = 'fixed'
            self.__on_command_button_click(self.__command_buttons_events[1], True)
        elif mode == 'morph':
            self.__mode = 'morph'
            self.__on_command_button_click(self.__command_buttons_events[2], True)
        elif mode == 'blink':
            self.__mode = 'blink' 
            self.__on_command_button_click(self.__command_buttons_events[3], True)
        else:
            print_warning('wrong mode={}'.format(mode))

    def get_hex_id(self):
        return self.__hex_id

    def get_area_name(self):
        return self.__area_name

    def get_column(self):
        return self.__column

    def get_mode(self):
        return self.__mode

    def get_left_color(self):
        return "#{0:02x}{1:02x}{2:02x}".format(int(self.__left_color.red * 255),  int(self.__left_color.green * 255),  int(self.__left_color.blue * 255))

    def get_right_color(self):
        return "#{0:02x}{1:02x}{2:02x}".format(int(self.__right_color.red * 255),  int(self.__right_color.green * 255),  int(self.__right_color.blue * 255))
            
    def set_right_color(self, hex_color):

        gdk_color = Gdk.RGBA()
        if gdk_color.parse(hex_color):
            self.__right_color = gdk_color

    def set_left_color(self, hex_color):

        gdk_color = Gdk.RGBA()
        if gdk_color.parse(hex_color):
            self.__left_color = gdk_color
    
                
# I ignore why this wasn't possible to be defined at __init__ as same as the ColorChooserToolbar 
GObject.type_register(ZoneWidget)
GObject.signal_new('updated', ZoneWidget, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())

GObject.type_register(ZoneWidget)
GObject.signal_new('request-delete', ZoneWidget, GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
                