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

import os
from shutil import rmtree

from AKBL.utils import getuser


class Paths:

    def __init__(self, user=getuser()):

        ## System
        ##
        self.COMPUTERS_CONFIGURATION_FOLDER = "/usr/share/AKBL/computers"
        self.DAEMON_PYRO_PATH = '/etc/akbl-daemon-adress'
        self.SYSTEMCTL_PATH = '/bin/systemctl'
        self.MAIN = '/usr/lib/python3/AKBL'

        ## User
        ##
        
        if user == 'root':
            self.CONFIGURATION_PATH = '/root/.config/alienware-kbl.ini'
            self.PROFILES_PATH = '/root/.local/share/alienware-kbl/'
        else:
            self.CONFIGURATION_PATH = '/home/{}/.config/alienware-kbl.ini'.format(user)
            self.PROFILES_PATH = '/home/{}/.local/share/alienware-kbl/'.format(user)
        
        ## GUI
        ##
        self.GLADE_FILE = '{}/ADDONS/GUI/GUI.glade'.format(self.MAIN)
        
        ## Block testing window
        ##
        self.BLOCK_TESTING_GLADE_FILE = '{}/ADDONS/BlockTesting/BlockTesting.glade'.format(self.MAIN)
        
        ## GUI & Others
        ##
        self.IMAGES = '{}/ADDONS/GUI/images/'.format(self.MAIN)
        self.SMALL_ICON = self.IMAGES + 'icon.png'
        self.MEDIUM_ICON = self.IMAGES + 'icon-m.png'

        ## Indicator
        ##
        self.INDICATOR_IMAGES_DIR = '{}/ADDONS/Indicator/images/'.format(self.MAIN)
        self.INDICATOR_ON_ICON = self.INDICATOR_IMAGES_DIR + 'icon-on.png'
        self.INDICATOR_OFF_ICON = self.INDICATOR_IMAGES_DIR + 'icon-off.png'
        self.INDICATOR_NO_DAEMON_ICON  = self.INDICATOR_IMAGES_DIR + 'icon-no-daemon.png'


        
        """
            This is to add support to older versions where the profiles and
            config was stored in the same directory than the code
        """
        self.BACKUP_CONFIG = '/etc/alienware-kbl/alienware-kbl.ini'
        self.BACKUP_PROFILES = '/etc/alienware-kbl/profiles/'
        self.GLOBAL_CONFIG = '/etc/alienware-kbl/gobal-config.ini'


        """
            Create the tree dirs
        """

        # In case there be a folder instead of the configuration file, delete the folder. Bug #84 
        # Old versions of alienware-kbl may still creating the folder. The bug was in the Paths class.
        #
        
        if os.path.isdir(self.CONFIGURATION_PATH):
            rmtree(self.CONFIGURATION_PATH)
        #
        #
        for dir_path in (os.path.dirname(self.CONFIGURATION_PATH), self.PROFILES_PATH):
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
