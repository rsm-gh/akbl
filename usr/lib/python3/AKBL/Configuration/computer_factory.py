#!/usr/bin/python3
#

#  Copyright (C) 2018  Rafael Senties Martinelli 
#
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
from configparser import ConfigParser

from AKBL.Configuration.Computer import Computer
from AKBL.Configuration.Region import Region
from AKBL.utils import print_debug, print_warning

def get_computers():

    computers = []
    
    path='/usr/share/AKBL/computers'
    
    for file_name in os.listdir(path):
        if file_name.endswith(".ini"):
            
            file_path=path+"/"+file_name
            
            print_debug("Reading {}".format(file_path))
            
            computer = Computer()
            
            config = ConfigParser()
            config.optionxform = str
            config.read(file_path)
    
            for key in config["COMMON"]:
                if hasattr(computer, key):
                    
                    value = config["COMMON"][key]
                    
                    if value != "":
                        if key in ("NAME","DEFAULT_COLOR","DEFAULT_MODE"):
                            setattr(computer, key, value)    
                        else:
                            setattr(computer, key, int(value))
                            
                            
            for section in config.sections():
                if section.startswith("REGION"):
                    region = Region(config[section]["ID"],
                                    config[section]["DESCRIPTION"],
                                    int(config[section]["BLOCK"]),
                                    int(config[section]["SUPPORTED_COMMANDS"]),
                                    config[section]["CAN_BLINK"]=="True",
                                    config[section]["CAN_MORPH"]=="True",
                                    config[section]["CAN_LIGHT"]=="True")
                    
                    computer.add_region(region)
                    
            
            add = True
            for added_computer in computers:
                if computer.NAME == added_computer:
                    print_warning("Computer name already exists={}".format(computer.NAME))
                    add = False
                    break
            
            if add:
                computers.append(computer)
    
    
    computers.sort(key= lambda computer: computer.NAME)
    
    return computers



def get_computer(name):
    
    for computer in get_computers():
        if computer.NAME == name:
            return computer
        
    return None
    
    
