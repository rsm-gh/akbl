#!/usr/bin/python3
#

#  Copyright (C) 2014-2018 Rafael Senties Martinelli.
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


def get_text_gtk_buffer(textbuffer):
    return textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), True)


def gtk_append_text_to_buffer(textbuffer, text):
    textbuffer.set_text(get_text_gtk_buffer(textbuffer) + text)


def gtk_dialog_question(parent, text1, text2=None, icon=None):
    dialog = Gtk.MessageDialog(parent,
                               Gtk.DialogFlags.MODAL,
                               Gtk.MessageType.QUESTION,
                               Gtk.ButtonsType.YES_NO,
                               text1)

    if icon is not None:
        dialog.set_icon_from_file(icon)

    if text2 is not None:
        dialog.format_secondary_text(text2)

    response = dialog.run()
    if response == Gtk.ResponseType.YES:
        dialog.hide()
        return True

    elif response == Gtk.ResponseType.NO:
        dialog.hide()
        return False


def gtk_dialog_info(parent, text1, text2=None, icon=None):
    dialog = Gtk.MessageDialog(parent,
                               Gtk.DialogFlags.MODAL,
                               Gtk.MessageType.INFO,
                               Gtk.ButtonsType.CLOSE,
                               text1)

    if icon is not None:
        dialog.set_icon_from_file(icon)

    if text2 is not None:
        dialog.format_secondary_text(text2)

    dialog.run()
    dialog.destroy()


def gtk_file_chooser(parent, title='', icon_path=None, default_folder=None, filters=None):

    if filters is None:
        filters = []

    window = Gtk.FileChooserDialog(title,
                                   parent,
                                   Gtk.FileChooserAction.OPEN,
                                   (Gtk.STOCK_CANCEL,
                                               Gtk.ResponseType.CANCEL,
                                               Gtk.STOCK_OPEN,
                                               Gtk.ResponseType.OK))

    window.set_default_response(Gtk.ResponseType.NONE)
    window.set_transient_for(parent)

    if icon_path is not None:
        window.set_icon_from_file(icon_path)

    if default_folder is not None:
        window.set_current_folder(default_folder)

    for filter_name, filter_extension in filters:
        gtk_filter = Gtk.FileFilter()
        gtk_filter.set_name(filter_name)
        gtk_filter.add_pattern(filter_extension)
        window.add_filter(gtk_filter)

    response = window.run()
    if response == Gtk.ResponseType.OK:
        file_path = window.get_filename()
        window.destroy()

        return file_path
    else:
        window.destroy()
        return False


def gtk_folder_chooser(parent, title='', icon_path=None, default_folder=None):
    window = Gtk.FileChooserDialog(
        title,
        parent,
        Gtk.FileChooserAction.SELECT_FOLDER,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

    if icon_path is not None:
        window.set_icon_from_file(icon_path)

    if default_folder is not None:
        window.set_current_folder(default_folder)

    response = window.run()
    if response == Gtk.ResponseType.OK:
        folder_path = window.get_filename()
        window.destroy()

        return folder_path
    else:
        window.destroy()
        return False
