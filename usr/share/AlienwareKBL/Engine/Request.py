#!/usr/bin/python3
#

#  Copyright (C)  2014-2017  Rafael Senties Martinelli <rafael@senties-martinelli.com>
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

from utils import print_debug

class Request:

    def __init__(self, legend, packet):

        self.legend = legend
        self.packet = packet  #[int(item) for item in packet]

    def __str__(self):
        
        formatted_package = "packet=["+'|'.join(str(item).rjust(3) for item in self.packet)+"]"
        
        return formatted_package+"\t legend={}".format(self.legend)
