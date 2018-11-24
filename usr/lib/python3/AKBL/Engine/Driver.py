#!/usr/bin/python3
#

#  Copyright (C)  2014-2018  RSM
#                 2011-2012  the pyAlienFX team
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


import sys
import usb
from traceback import format_exc

from AKBL.utils import print_debug, print_error
from AKBL.Data.Computer import factory as computer_factory
from AKBL.Data.Computer.Computer import Computer


class Driver:

    def __init__(self):
        
        # Define I/O Reqquest types
        self.SEND_REQUEST_TYPE = 33
        self.SEND_REQUEST = 9
        self.SEND_VALUE = 514
        self.SEND_INDEX = 0
        self.READ_REQUEST_TYPE = 161
        self.READ_REQUEST = 1
        self.READ_VALUE = 257
        self.READ_INDEX = 0
        
        self._device = None
        
        self.computer = computer_factory.get_default_computer()
        
        if self.computer is not None:
            self.load_device(self.computer.VENDOR_ID, self.computer.PRODUCT_ID)
        

    def has_device(self):
        if self._device is None:
            return False
        return True

    def find_device(self):
        """
            Look for all the devices listed in the `Computers.py` file.
            If a computer is finded, the device is loaded as well as 
            all its parameters.
        """

        for computer in computer_factory.get_computers():

            device = usb.core.find(idVendor=computer.VENDOR_ID, idProduct=computer.PRODUCT_ID)

            if device is not None:
                
                self._device = device
                self.take_over()

                self.computer = computer
                
                print_debug(device)
                print_debug(self.computer)


    def load_device(self, id_vendor, id_product, empty_computer=False):
        """
            Load a device from given'ids and then if success load
            the global computer configuration. 
            
            This is used at the block_testing_window for testing new computers.
        """

        device = usb.core.find(idVendor=id_vendor, idProduct=id_product)

        if device is not None:
            self._device = device
            self.take_over()
            print_debug('{}'.format(device))
            
        if empty_computer:    
            self.computer = Computer()

    def write_constructor(self, constructor):
        
        print_debug('\n'.join(str(request) for request in constructor))
        
        for command in constructor:
            self._device.ctrl_transfer(self.SEND_REQUEST_TYPE, 
                                       self.SEND_REQUEST, 
                                       self.SEND_VALUE, 
                                       self.SEND_INDEX, 
                                       command)

    def read_device(self, constructor):
        
        msg = self._device.ctrl_transfer(self.READ_REQUEST_TYPE, 
                                         self.READ_REQUEST, 
                                         self.READ_VALUE, 
                                         self.READ_INDEX, 
                                         len(constructor.get_first_command()))

        print_debug("msg={}".format(msg))

        return msg

    def take_over(self):
        try:
            self._device.set_configuration()
        except:
            self._device.detach_kernel_driver(0)
            try:
                self._device.set_configuration()
            except Exception:
                print_error(format_exc())
                sys.exit(1)
