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

_LEFT_CLICK = 1
_RIGHT_CLICK = 3


def norm_color(color):
    
    doit = False
    for i in color:
        if i > 1:
            doit = True
    for i in range(0, len(color)):
        color[i] = color[i] / 255.0
    return color


def middle_color(color1, color2):
    return [((color1[0] + color2[0]) / 2.0),
            ((color1[1] + color2[1]) / 2.0),
            ((color1[2] + color2[2]) / 2.0)]


def get_rgb_list(gdk3_rgba_object):
    """
        Returns a list of the RGB values of an Gdk.RGBA object.
        Ex: `Gdk.RGBA(red=0.937255, green=0.160784, blue=0.160784, alpha=1.000000)` to `[0.937255, 0.160784, 0.160784]`
        
        I'd like to do this properly, with something like `[gdk3_rgba_object.red(), gdk3_rgba_object.green(), gdk3_rgba_object.blue()]`
        but I didn't find the solution. Some doc at:
        
            https://developer.gnome.org/gdk3/stable/gdk3-RGBA-Colors.html#gdk-rgba-to-string
    """

    rgb_list = []

    gdk3_rgb_str_items = str(gdk3_rgba_object).split('=')
    for item in gdk3_rgb_str_items:
        if '.' in item:
            for subitem in item.split(','):
                if '(' not in subitem and ')' not in subitem and '.' in subitem:
                    rgb_list.append(float(subitem))

    return rgb_list


def hex_to_rgb(string):
    """ 
        Convert hex color strings to an RGB list. 
        Ex:  `0000FF` to `[0, 0, 255]` 
    """

    if string.startswith('#'):
        string = string.lstrip('#')
        
    lv = len(string)
    r, g, b = tuple(int(string[i:i + lv // 3], 16)
                    for i in range(0, lv, lv // 3))
                    
    return [r, g, b]


class Zone(Gtk.Frame):

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

    def __init__(
            self,
            color1,
            color2,
            colorchooser,
            zone,
            column,
            colorchooser2=False,
            *args,
            **kwds):

        super(self.__class__, self).__init__(*args, **kwds)

        # Variables
        #
        self.id = None
        self.color1 = False
        self.color2 = False
        self.heigth = 100
        self.width = 90
        # this indicates to the THREAD_zones if there has been changes
        self.color_updated = False
        self.mode = 'fixed'
        self.commands_buttons_state = [
            False, True, False, False]  # delete, fixed, morph, blink

        # Created Gtk objects
        box = Gtk.Box()
        box.set_size_request(-1, -1)

        # requested objects and variables
        #
        self.colorchooserdialog = colorchooser
        self.colorchooserwidget2 = colorchooser2

        if zone is not None:
            self.zone = zone
        else:
            self.zone = False

        self.set_color(color1, 1)
        self.set_color(color2, 2)

        self.commands_buttons_box = Gtk.VBox()

        # Initialize the drawing areas
        #
        self.darea1, self.darea2 = Gtk.DrawingArea(), Gtk.DrawingArea()

        self.darea1.set_size_request(self.width, self.heigth)
        self.darea2.set_size_request(self.width, self.heigth)

        self.darea1.connect('draw', self.create_gradient, 1)
        self.darea2.connect('draw', self.create_gradient, 2)

        self.darea1.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.darea2.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self.darea1.connect('button-press-event', self.on_drawingarea_click, 1)
        self.darea2.connect('button-press-event', self.on_drawingarea_click, 2)

        self.set_column(column)

        box.pack_start(self.darea1, False, False, 0)
        box.pack_start(self.darea2, False, False, 0)
        box.pack_start(self.commands_buttons_box, False, False, 0)
        self.add(box)
        self.show_all()

    def set_column(self, column):

        # The removed parts of the code enable the power button/eyes names.
        # bug(#100)
        '''
        blocks=['A/C Power','Battery Critical','Battery Power','Battery Sleeping','Charging','Load on Boot','Standby']
        '''

        self.column = column

        if self.zone:
            '''
            if not 'Power' in self.zone.description:
            '''
            if True:
                if column % 2 == 0:
                    self.set_label(self.zone.description)
                else:
                    self.set_label(' ')
            '''
            else:
                if 'Eyes' in self.zone.description:
                    label = 'PB Eyes:'
                else:
                    label = 'PowerButton:'
                self.set_label(label+'   '+blocks[column])
            '''
        else:
            self.set_label("Column {}".format(column))

        self.init_commands_box()

    def set_mode(self, mode):
        """
            This is only for initializing the zone from the configuration file
        """
        if mode == 'morph':
            self.mode = 'morph'
            self.on_command_button_click(self.commands_buttons_events[2], True)
        elif mode == 'blink':
            self.mode = 'blink'
            self.on_command_button_click(self.commands_buttons_events[3], True)

    def set_color(self, color, widget_zone):

        if isinstance(color, str):
            color = hex_to_rgb(color)

        if widget_zone == 1:
            self.color1 = norm_color(color)
        else:
            self.color2 = norm_color(color)

        if self.color2:
            self.color3 = middle_color(self.color1, self.color2)

    def init_commands_box(self):

        # Remove the previous content
        for children in self.commands_buttons_box.get_children():
            self.commands_buttons_box.remove(children)
        self.commands_buttons_events = []

        # Populate
        for i in (4, 1, 6, 7):
            event_box = Gtk.EventBox()
            event_box.add(self.command_buttons_get_image(i))

            if i == 4 and self.column <= 0:
                pass
            else:
                event_box.connect(
                    'button-press-event',
                    self.on_command_button_click)

            self.commands_buttons_box.pack_start(event_box, False, False, 0)
            self.commands_buttons_events.append(event_box)

        self.update_commands_buttons_background()
        self.commands_buttons_box.show_all()

    def on_drawingarea_click(self, widget, event, area_number):

        key = event.button

        if key is not _LEFT_CLICK and key is not _RIGHT_CLICK:
            return

        elif key == _LEFT_CLICK:

            if not self.colorchooserwidget2 or not self.colorchooserwidget2.get_property(
                    'visible'):
                response = self.colorchooserdialog.run()
                if response == Gtk.ResponseType.OK:
                    color = get_rgb_list(self.colorchooserdialog.get_rgba())
                else:
                    color = False

                self.colorchooserdialog.hide()

            else:
                color = get_rgb_list(self.colorchooserwidget2.get_rgba())

            if color:

                if area_number == 1 or not self.commands_buttons_state[
                        2]:  # morph
                    self.color1 = color
                else:
                    self.color2 = color

                self.color3 = middle_color(self.color1, self.color2)
                self.color_updated = True
                self.create_gradient(widget, self.cr, 1)

        elif key == _RIGHT_CLICK:

            color = get_rgb_list(self.colorchooserdialog.get_rgba())

            if area_number == 1 or not self.commands_buttons_state[2]:  # morph
                self.color1 = color
            else:
                self.color2 = color

            self.color3 = middle_color(self.color1, self.color2)

            self.create_gradient(self.darea1, self.cr, 1)
            self.color_updated = True
            self.create_gradient(self.darea2, self.cr, 2)

        self.update_commands_buttons_background()

    def on_command_button_click(self, widget, data=None):

        old_mode = self.mode

        for i in range(4):
            # Remove the buttons
            event_box = self.commands_buttons_events[i]
            event_box.remove(event_box.get_children()[0])

            # Populate with new images
            if event_box == widget:
                event_box.add(self.command_buttons_get_image(i))
                self.commands_buttons_state[i] = True

                if i == 0:
                    self.mode = 'delete'
                elif i == 1:
                    self.mode = 'fixed'
                elif i == 2:
                    self.mode = 'morph'
                elif i == 3:
                    self.mode = 'blink'

                if self.mode != old_mode and self.mode != 'delete':
                    self.color_updated = True

            else:
                event_box.add(self.command_buttons_get_image(i + 4))
                self.commands_buttons_state[i] = False

        self.update_commands_buttons_background()
        self.commands_buttons_box.show_all()

    def command_buttons_get_image(self, number):

        if self.column == 0 or (self.zone and 'PB' in self.zone.name):
            paths = [
                'empty',
                'fixed_on',
                'morph_on',
                'blink_on',
                'empty',
                'fixed_off',
                'morph_off',
                'blink_off']
        else:
            paths = [
                'cross_on',
                'fixed_on',
                'morph_on',
                'blink_on',
                'cross_off',
                'fixed_off',
                'morph_off',
                'blink_off']

        return Gtk.Image.new_from_file('./images/' + paths[number] + '.png')

    def create_gradient(self, widget, cr, area_number):

        self.cr = cr

        if self.commands_buttons_state[2]:  # morph
            if area_number == 1:
                start = self.color1
                stop = self.color3
            if area_number == 2:
                start = self.color3
                stop = self.color2
        else:
            start, stop = self.color1, self.color1
            self.update_commands_buttons_background()

        lg1 = cairo.LinearGradient(0.0, 0.0, self.width, 0)
        lg1.add_color_stop_rgb(0, start[0], start[1], start[2])
        lg1.add_color_stop_rgb(1, stop[0], stop[1], stop[2])
        self.cr.rectangle(0, 0, self.width, self.heigth)
        self.cr.set_source(lg1)
        self.cr.fill()
        widget.queue_draw_area(0, 0, 100, 100)

        return True

    def update_commands_buttons_background(self):

        if self.commands_buttons_state[2]:  # morph
            color = self.color2
        else:
            color = self.color1

        for children in self.commands_buttons_box.get_children():
            for child in children.get_children():
                child.override_background_color(
                    Gtk.StateType.NORMAL, Gdk.RGBA(
                        color[0], color[1], color[2], 1))

        self.commands_buttons_box.override_background_color(
            Gtk.StateType.NORMAL, Gdk.RGBA(color[0], color[1], color[2], 1))


if __name__ == '__main__':

    # Create the GTK Interface
    #
    w = Gtk.Window()
    w.set_size_request(900, 300)
    sw = Gtk.ScrolledWindow()
    grid = Gtk.Grid()
    vp = Gtk.Viewport()
    cc = Gtk.ColorChooserDialog()
    vp.add(grid)
    sw.add(vp)
    w.add(sw)

    # Add the Zone objects to be tested
    #
    for row in range(2):
        fixed_zone = Zone('#020202', [255, 34, 122], cc, None, 0)
        # widget, column, row, column width, row width
        grid.attach(fixed_zone, 0, row, 1, 1)

    blink_zone = Zone([122, 255, 22], [255, 34, 122], cc, None, 1)
    blink_zone.set_mode('blink')
    grid.add(blink_zone)

    morph_zone = Zone([122, 255, 22], [255, 34, 122], cc, None, 2)
    morph_zone.set_mode('morph')
    grid.add(morph_zone)

    # Launch of the Interface
    #
    w.show_all()
    Gtk.main()
