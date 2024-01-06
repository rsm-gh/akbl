#!/usr/bin/python3
#

#  Copyright (C) 2015-2019 Rafael Senties Martinelli.
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
import shutil

from AKBL.utils import getuser


class Paths:

    def __init__(self, user=getuser()):

        ## System
        ##
        self._akbl_share_dir = '/usr/share/AKBL'
        self._computers_configuration_dir = "/usr/share/AKBL/computers"
        self._default_computer_file = '/etc/AKBL/default_computer.ini'
        self._daemon_pyro_file = '/etc/AKBL/pyro-address'

        ## User
        ##


        if user == 'root':
            self._configuration_file = '/root/.config/akbl.ini'
            self._profiles_dir = '/root/.local/share/akbl/'
        else:
            self._configuration_file = '/home/{}/.config/akbl.ini'.format(user)
            self._profiles_dir = '/home/{}/.local/share/akbl/'.format(user)

        # The paths went renamed from "alienware-kbl" to "akbl", this will migrate the data.
        for location in (self._configuration_file, self._profiles_dir):
            old_location = location.replace("akbl", "alienware-kbl")
            if os.path.exists(old_location):
                os.rename(old_location, location)


        ## GUI & Others
        ##
        self._icon_file = os.path.join(self._akbl_share_dir, 'icon.png')

        """
            Create the necessary folders.
        """

        #
        # Create the system folders
        #
        if user == 'root':
            system_write_folders = [
                os.path.dirname(self._default_computer_file),
                os.path.dirname(self._daemon_pyro_file)]

            for dir_path in system_write_folders:
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

        #
        # Create the user folders
        #
        for dir_path in (os.path.dirname(self._configuration_file), self._profiles_dir):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

        #
        # Bug #84: In case there be a folder instead of the configuration file, delete the folder.  
        # Old versions of alienware-kbl may still create the folder, the bug was in the Paths class.
        #
        if os.path.isdir(self._configuration_file):
            shutil.rmtree(self._configuration_file)
