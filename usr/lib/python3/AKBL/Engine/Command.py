#!/usr/bin/python3
#

#  Copyright (C) 2014-2020 Rafael Senties Martinelli.
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

class Command(object):

    def __init__(self, legend, command):

        self.__legend = legend
        self.__command = command  #[int(item) for item in packet]

    def __str__(self):
        formatted_package = "packet="+':'.join(str(item) for item in self.__command)
        return formatted_package+"\t legend={}".format(self.__legend)

    def __iter__(self):
        for item in self.__command:
            yield item
            
    def __len__(self):
        return len(self.__command)
