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


class Command:

    def __init__(self, legend: str, command: list[int]) -> None:
        self.__legend = legend
        self.__command = command

    def __str__(self) -> str:
        return f"[{','.join(str(item) for item in self.__command)}] \t {self.__legend}"

    def __iter__(self):
        for item in self.__command:
            yield item

    def __len__(self) -> int:
        return len(self.__command)
