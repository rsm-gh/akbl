#!/usr/bin/python3
#

#  Copyright (C) 2024 Rafael Senties Martinelli.
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

from console_printer import print_debug


class FakeUSB:
    """This class is for debugging in computers that are not alienware."""

    def __init__(self):
        from AKBL.Computer.Computer import Computer
        self.__computer = Computer()

    def ctrl_transfer(self, *args):
        #print_debug()
        #for arg in args:
        #    print_debug(str(arg), direct_output=True)
        return [self.__computer.state_ready]

    @staticmethod
    def set_configuration():
        #print_debug()
        pass

    @staticmethod
    def detach_kernel_driver(*args):
        #print_debug(str(args))
        pass

