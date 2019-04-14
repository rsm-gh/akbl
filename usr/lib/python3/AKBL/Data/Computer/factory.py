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

from AKBL.Paths import Paths; _SOFTWARE_PATHS = Paths()
from AKBL.Data.Computer.Computer import Computer
from AKBL.Data.Computer.Region import Region
from AKBL.utils import print_debug, print_warning, print_error



def get_computer_by_path(file_path):

    print_debug("Reading {}".format(file_path))
    
    computer = Computer()
    computer.configuration_path = file_path
    
    config = ConfigParser()
    config.optionxform = str
    
    try:
        config.read(file_path)
    except:
        print_error("Corrupted file: {}".format(file_path))
        return None
        
    
    for key in config["COMMON"]:
        if hasattr(computer, key):
            
            value = config["COMMON"][key]
            
            if value != "":
                if key in ("NAME","DEFAULT_MODE"):
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

    return computer


def get_computers():

    computers = []
    
    path=Paths()._computers_configuration_dir
    
    for file_name in os.listdir(path):
        if file_name.endswith(".ini"):
            
            file_path=path+"/"+file_name
            
            computer = get_computer_by_path(file_path)
            
            if not computer is None:            
                add = True
                for added_computer in computers:
                    if computer.NAME == added_computer:
                        print_warning("Computer name already exists={}".format(computer.NAME))
                        add = False
                        break
                
                if add:
                    computers.append(computer)
    
    
    computers.sort(key=lambda computer: computer.NAME)
    
    return computers


def get_default_computer():
    
    default_computer_path = _SOFTWARE_PATHS._default_computer_file
    
    if not os.path.exists(default_computer_path):
        return None
        
    return get_computer_by_path(default_computer_path)

def set_default_computer(computer_name):
    
    for computer in get_computers():
        if computer.NAME == computer_name:
            with open(_SOFTWARE_PATHS._default_computer_file, 'w') as fw:
                with open(computer.configuration_path, 'r') as fr:
                    fw.write(fr.read())
            
            print("Default computer updated to: {}".format(computer_name))
            return
    

def get_computer(name):
    
    for computer in get_computers():
        if computer.NAME == name:
            return computer
        
    return None
    
    
