#!/usr/bin/python3
#

#  Copyright (C) 2014-2024 Rafael Senties Martinelli.
#                2011-2012 the pyAlienFX team.
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


import usb
from traceback import format_exc

from Engine import Constructor
from Engine.FakeUSB import FakeUSB
from console_printer import print_debug, print_error


class Driver:

    def __init__(self, fake: bool = False):

        self.__usb_device = None
        self.__fake = fake

        # Define I/O Request types
        self.__send_request_type = 33
        self.__send_request = 9
        self.__send_value = 514
        self.__send_index = 0
        self.__read_request_type = 161
        self.__read_request = 1
        self.__read_value = 257
        self.__read_index = 0

    def load_device(self, id_vendor: int, id_product: int) -> None:

        print_debug(f"id_vendor={id_vendor}, id_product={id_product}")

        if self.__fake:
            print_debug(f'faking usb device...', direct_output=True)
            self.__usb_device = FakeUSB()
        else:
            try:
                self.__usb_device = usb.core.find(idVendor=id_vendor, idProduct=id_product)
            except Exception:
                self.__usb_device = None
                print_error(format_exc())

            print_debug(f'usb_device={self.__usb_device}', direct_output=True)

        if self.__usb_device is not None:
            self.take_over()

    def has_device(self) -> None | bool:
        if self.__usb_device is None:
            return False
        return True

    def device_information(self) -> str:
        return str(self.__usb_device)

    def write_constructor(self, constructor: Constructor) -> None:
        # Todo: read the status?

        print_debug('\n'.join(str(request) for request in constructor))

        try:
            for command in constructor:
                status = self.__usb_device.ctrl_transfer(self.__send_request_type,
                                                         self.__send_request,
                                                         self.__send_value,
                                                         self.__send_index,
                                                         command)

                if not self.__fake:
                    print_debug(f"command output={status}")

        except Exception:
            print_error(format_exc())

    def read_device(self, constructor: Constructor) -> None | int:

        print_debug(str(constructor))

        try:
            msg = self.__usb_device.ctrl_transfer(self.__read_request_type,
                                                  self.__read_request,
                                                  self.__read_value,
                                                  self.__read_index,
                                                  len(constructor.get_first_command()))

        except Exception:
            print_error(format_exc())
            return None

        if not self.__fake:
            print_debug(f"msg={msg}")

        return msg

    def take_over(self) -> None:

        print_debug()

        try:
            self.__usb_device.set_configuration()
        except Exception:
            self.__usb_device.detach_kernel_driver(0)
            try:
                self.__usb_device.set_configuration()
            except Exception:
                print_error(format_exc())
