#!/usr/bin/python3
#

#  Copyright (C) 2015-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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
import cairo

import sys
sys.path.insert(0, "/usr/share/AlienwareKBL")
from Configuration.Paths import Paths
from utils import middle_rgb_color, print_warning


_IMAGES_PATH = Paths().IMAGES
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

        Usage:

            > To change a color left-click on the drawing area and then use the color chooser.
            > To use the last selected color, just right-click on the drawing area.
    """

    __gtype_name__ = 'Zone'

    def __init__(self, area_name, left_color, right_color, mode, column, colorchooser_widget, hex_id=1):

        super().__init__()

        # Variables
        #
        self._left_color = []
        self._right_color = []
        self._mode = ''
        
        self._hex_id = ''
        self._area_name = ''

        self._heigth = 100
        self._width = 90

        self.color_updated = False  # Pretty important to know if the widget has been updated
        self._commands_buttons_events = []
        self._commands_buttons_state = [False,  # Delete button
                                        True,   # Fixed button
                                        False,  # Morph button
                                        False]  # Blink button



        # requested objects and variables
        #
        self._color_chooser_widget = colorchooser_widget
        self.zone = None

        self.set_color(left_color, 'left')
        self.set_color(right_color, 'right')

        self._commands_buttons_box = Gtk.VBox()

        # Create the Gtk objects
        #
        box = Gtk.Box()
        box.set_size_request(-1, -1)

        self._drawing_area1 = Gtk.DrawingArea()
        self._drawing_area2 = Gtk.DrawingArea()

        self._drawing_area1.set_size_request(self._width, self._heigth)
        self._drawing_area2.set_size_request(self._width, self._heigth)

        self._drawing_area1.connect('draw', self._create_gradient, 1)
        self._drawing_area2.connect('draw', self._create_gradient, 2)

        self._drawing_area1.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self._drawing_area2.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self._drawing_area1.connect('button-press-event', self._on_drawingarea_click, 1)
        self._drawing_area2.connect('button-press-event', self._on_drawingarea_click, 2)

        # Finish the GTK interface
        #
        box.pack_start(child=self._drawing_area1, expand=False, fill=False, padding=0)
        box.pack_start(child=self._drawing_area2, expand=False, fill=False, padding=0)
        box.pack_start(child=self._commands_buttons_box, expand=False, fill=False, padding=0)
        self.add(box)
        self.show_all()

        # Extra initialization
        #
        self.set_column(column)
        self.set_mode(mode)
        self.set_area_name(area_name)
        self.set_hex_id(hex_id)

    def _init_commands_box(self):

        # Remove the previous content
        for children in self._commands_buttons_box.get_children():
            self._commands_buttons_box.remove(children)
        self._commands_buttons_events = []

        # Populate
        for i in (4, 1, 6, 7):
            event_box = Gtk.EventBox()
            event_box.add(self._get_command_button_image(i))

            if i == 4 and self._column <= 0:
                pass
            else:
                event_box.connect('button-press-event', self._on_command_button_click)

            self._commands_buttons_box.pack_start(event_box, False, False, 0)
            self._commands_buttons_events.append(event_box)

        self._update_commands_buttons_background()
        self._commands_buttons_box.show_all()

    def _on_drawingarea_click(self, widget, event, area_number):

        if event.button == _LEFT_CLICK_ID:

            color = self._color_chooser_widget.get_rgba()

            if color:

                if area_number == 1 or not self._commands_buttons_state[2]:  # morph
                    self._left_color = color
                else:
                    self._right_color = color

                self._create_gradient(widget, self.cr, 1)
                self.color_updated = True

        self._update_commands_buttons_background()

    def _on_command_button_click(self, widget, data=None):

        old_mode = self._mode

        for i in range(4):
            # Remove the buttons
            event_box = self._commands_buttons_events[i]
            event_box.remove(event_box.get_children()[0])

            # Populate with new images
            if event_box == widget:
                event_box.add(self._get_command_button_image(i))
                self._commands_buttons_state[i] = True

                if i == 0:
                    self._mode = 'delete'
                elif i == 1:
                    self._mode = 'fixed'
                elif i == 2:
                    self._mode = 'morph'
                elif i == 3:
                    self._mode = 'blink'

                if self._mode != old_mode and self._mode != 'delete':
                    self.color_updated = True

            else:
                event_box.add(self._get_command_button_image(i + 4))
                self._commands_buttons_state[i] = False

        self._update_commands_buttons_background()
        self._commands_buttons_box.show_all()

    def _get_command_button_image(self, index):

        if self._column == 0 or self._area_name in ('PB','PBE'):
            return Gtk.Image.new_from_file('{}{}.png'.format(_IMAGES_PATH, _BUTTONS_IMAGE_PATTERN[index]))

        return Gtk.Image.new_from_file('{}{}.png'.format(_IMAGES_PATH, _BUTTONS_IMAGE_PATTERN_WITH_DELETE[index]))

    def _create_gradient(self, widget, cr, area_number):

        self.cr = cr

        if self._commands_buttons_state[2]:  # morph
            
            middle_color=middle_rgb_color((self._left_color.red, self._left_color.green, self._left_color.blue),
                                          (self._right_color.red, self._right_color.green, self._right_color.blue))
            
            middle_color = Gdk.RGBA(*middle_color)
            
            if area_number == 1:
                start_color = self._left_color
                end_color = middle_color
            if area_number == 2:
                start_color = middle_color
                end_color = self._right_color
        else:
            start_color = self._left_color
            end_color =  self._left_color
            self._update_commands_buttons_background()


        lg1 = cairo.LinearGradient(0.0, 0.0, self._width, 0)
        lg1.add_color_stop_rgb(0, start_color.red, start_color.green, start_color.blue)
        lg1.add_color_stop_rgb(1, end_color.red, end_color.green, end_color.blue)
        self.cr.rectangle(0, 0, self._width, self._heigth)
        self.cr.set_source(lg1)
        self.cr.fill()
        widget.queue_draw_area(0, 0, 100, 100)

        return True

    def _update_commands_buttons_background(self):

        if self._commands_buttons_state[2]:  # morph
            gdk_color = self._right_color
        else:
            gdk_color = self._left_color

        for children in self._commands_buttons_box.get_children():
            for child in children.get_children():
                child.override_background_color(Gtk.StateType.NORMAL, gdk_color)

        self._commands_buttons_box.override_background_color(Gtk.StateType.NORMAL, gdk_color)

    def set_hex_id(self, hex_id):
        self._hex_id = hex_id

    def set_area_name(self, area_name):
        self._area_name = area_name

    def set_column(self, column):
        self._column = column
        self._init_commands_box()

    def set_mode(self, mode):

        if mode == 'fixed':
            self._mode = 'fixed'
            self._on_command_button_click(self._commands_buttons_events[1], True)
        elif mode == 'morph':
            self._mode = 'morph'
            self._on_command_button_click(self._commands_buttons_events[2], True)
        elif mode == 'blink':
            self._mode = 'blink' 
            self._on_command_button_click(self._commands_buttons_events[3], True)
        else:
            print_warning('wrong mode={}'.format(mode))

    def get_hex_id(self):
        return self._hex_id

    def get_area_name(self):
        return self._area_name

    def get_column(self):
        return self._column

    def get_mode(self):
        return self._mode

    def get_left_color(self):
        return "#{0:02x}{1:02x}{2:02x}".format(int(self._left_color.red * 255),  int(self._left_color.green * 255),  int(self._left_color.blue * 255))

    def get_right_color(self):
        return "#{0:02x}{1:02x}{2:02x}".format(int(self._right_color.red * 255),  int(self._right_color.green * 255),  int(self._right_color.blue * 255))

    def set_color(self, hex_color, widget_zone):

        gdk_color = Gdk.RGBA()
        if gdk_color.parse(hex_color):

            if widget_zone == 'left':
                self._left_color = gdk_color
            elif widget_zone == 'right':
                self._right_color = gdk_color
            else:
                print_warning('wrong zone name='.format(widget_zone))

if __name__ == '__main__':

    #
    # THE FOLLOWING CODE IS ONLY FOR TESTING.
    #

    # Create the GTK Interface
    #
    ROOT_WINDOW = Gtk.Window(title="Zone widget test")
    ROOT_WINDOW.set_size_request(width=900, height=600)
    BOX = Gtk.VBox()
    GRID = Gtk.Grid()
    VIEWPORT = Gtk.Viewport()
    VIEWPORT.add(GRID)
    SCROLLED_WINDOW = Gtk.ScrolledWindow()
    SCROLLED_WINDOW.add(VIEWPORT)

    COLOR_CHOOSER_WIDGET = Gtk.ColorChooserWidget()

    def on_button_click(widget):
        """
            Hide or un-hide the `COLOR_CHOOSER_WIDGET` in
            order to test the `COLOR_CHOOSER_DIALOG`.
        """
        if COLOR_CHOOSER_WIDGET.get_property('visible'):
            COLOR_CHOOSER_WIDGET.set_visible(False)
        else:
            COLOR_CHOOSER_WIDGET.set_visible(True)

    BUTTON = Gtk.Button(label="Toggle the ColorChooserWidget")
    BUTTON.connect('clicked', on_button_click)

    BOX.pack_start(child=BUTTON, expand=False, fill=True, padding=10)
    BOX.pack_start(child=COLOR_CHOOSER_WIDGET, expand=False, fill=True, padding=10)
    BOX.pack_start(child=SCROLLED_WINDOW, expand=True, fill=True, padding=0)

    ROOT_WINDOW.add(BOX)

    # Add the Zone objects to be tested
    #
    for row_index in range(2):
        FIXED_ZONE = ZoneWidget(area_name='PB',
                                left_color='#020202',
                                right_color='#020202',
                                mode='fixed',
                                column=0,
                                colorchooser_widget=COLOR_CHOOSER_WIDGET)

        GRID.attach(child=FIXED_ZONE, left=0, top=row_index, width=1, height=1)

    BLINK_ZONE = ZoneWidget(area_name='',
                            left_color='#020202',
                            right_color='#020202',
                            mode='blink',
                            column=1,
                            colorchooser_widget=COLOR_CHOOSER_WIDGET)

    GRID.add(BLINK_ZONE)

    MORPH_ZONE = ZoneWidget(area_name='',
                            left_color='#020202',
                            right_color='#020202',
                            mode='morph',
                            column=2,
                            colorchooser_widget=COLOR_CHOOSER_WIDGET)

    GRID.add(MORPH_ZONE)

    # Launch the interface
    #
    ROOT_WINDOW.show_all()
    Gtk.main()
