#!/usr/bin/python3
#

#  Copyright (C)  2014-2017  Rafael Senties Martinelli 
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
import os
import time
import usb
from traceback import format_exc

# Local imports
sys.path.insert(0, "/usr/share/AlienwareKBL")
from utils import print_debug, print_error
from Configuration.Computers import Computer, AVAILABLE_COMPUTERS, M14XR1, M14XR2

class Driver():

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

        self.computer = None
        self._device = None
        
        self._device_found = False
        
        self.find_device()

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

        for computer in AVAILABLE_COMPUTERS:

            device = usb.core.find(idVendor=computer.VENDOR_ID, idProduct=computer.PRODUCT_ID)

            if device is not None:
                self._device = device
                self.take_over()
                print_debug(device)
                
                # This hack was made to differenciate the M14XR1 from the M14XR2R2
                if isinstance(computer, M14XR1) and 'Gaming' in str(device):
                    computer = M14XR2()

                self.computer = computer
                print_debug(self.computer)


    def load_device(self, id_vendor, id_product):
        """
            Load a device from given'ids and then if success load
            the global computer configuration. This is used at the block_testing_window
            for testing new computers.
        """

        device = usb.core.find(idVendor=id_vendor, idProduct=id_product)

        if device is not None:
            self._device = device
            self.take_over()
            print_debug('device loaded:\n{}'.format(device))
            self.computer = Computer()

    def write_constructor(self, constructor):
        
        print_debug('\n'.join(str(request) for request in constructor))
        
        for request in constructor:
            self._device.ctrl_transfer(self.SEND_REQUEST_TYPE, self.SEND_REQUEST, self.SEND_VALUE, self.SEND_INDEX, request.packet)
            time.sleep(0.01)

    def read_device(self, msg):
        
        msg = self._device.ctrl_transfer(self.READ_REQUEST_TYPE, self.READ_REQUEST, self.READ_VALUE, self.READ_INDEX, len(msg[0].packet))

        print_debug("msg={}".format(msg))

        return msg

    def take_over(self):
        try:
            self._device.set_configuration()
        except:
            self._device.detach_kernel_driver(0)
            try:
                self._device.set_configuration()
            except Exception as e:
                print_error(format_exc())
                sys.exit(1)
