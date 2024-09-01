#!/usr/bin/python3

#
# MIT License
#
# Copyright (c) 2014-2024 Rafael Senties Martinelli.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import ast
import traceback
import configparser
from typing import Any
from copy import deepcopy

__version__ = '0.6.6'


class CCParser(object):

    def __init__(self, ini_path: str = '', section: str = '', print_errors=True):
        """
            To init CCParser you can enter a path and a section.
            If you don't know them, you can leave them empty.

            If print_errors is set to True, all the exceptions
            will print their traceback.
        """
        self.__print_errors = print_errors
        self.__config = configparser.ConfigParser()

        self.__ini_path = ''
        if ini_path != '':
            self.set_configuration_path(ini_path)

        self.__section = ''
        if section != '':
            self.set_section(section)

        self.__default_bool = False
        self.__default_string = ''
        self.__default_int = 0
        self.__default_float = 0.0
        self.__default_list = []

        self.__accepted_true_bool = ('true', 'yes')
        self.__accepted_false_bool = ('false', 'no')

        self.__version__ = __version__

    def print_info(self) -> None:
        print('''
CCParser instance:
 Configuration Path: {}
 Section: {}
 Default boolean: {}
 Default float: {}
 Default integer: {}
 Default string: {}
'''.format(self.get_configuration_path(),
           self.get_section(),
           self.get_default_bool(),
           self.get_default_float(),
           self.get_default_int(),
           self.get_default_str()
           ))

    def check_value(self, value: str) -> bool:
        """
            return False if the value does not exist.
            return True if the value exists.
        """
        if os.path.exists(self.__ini_path):
            try:
                self.__config.read(self.__ini_path)
            except Exception:
                print("CCParser Warning: reading damaged file or file without section")
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                if self.__config.has_section(self.__section) and self.__config.has_option(self.__section, value):
                    return True

        return False

    def write(self, value_name: str, value: Any) -> None:
        """
            Write the value name and its value.

            If the config file does not exist,
            or the directories to the path, they
            will be created.
        """

        if self.__ini_path != '' and isinstance(self.__ini_path, str):

            if not os.path.exists(os.path.dirname(self.__ini_path)):
                os.makedirs(os.path.dirname(self.__ini_path))

            if not os.path.exists(self.__ini_path):
                open(self.__ini_path, 'w').close()

            try:
                self.__config.read(self.__ini_path)
            except Exception:
                print("CCParser Warning: reading damaged file or file without section")
                print(traceback.format_exc())
                print()

            if not self.__config.has_section(self.__section):
                self.__config.add_section(self.__section)

            self.__config.set(self.__section, value_name, str(value))

            with open(self.__ini_path, 'w') as f:
                self.__config.write(f)
        else:
            print("CCParser Error: Trying to write the configuration without an ini path.")
            print("Configuration Path: " + str(self.get_configuration_path()))
            print()

    def get_bool(self, value: str) -> bool:
        """
            If the value exists, return the boolean
            corresponding to the string.

            If it does not exist, or the value cannot be converted
            to a boolean, return the default boolean.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value).lower()
            if val in self.__accepted_true_bool:
                return True

            elif val in self.__accepted_false_bool:
                return False

        return self.__default_bool

    def get_float(self, value: str) -> float:
        """
            If the value exists, return the float
            corresponding to the string.

            If it does not exist, or the value cannot be converted to a float,
            return the default float.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value)
            try:
                val = float(val)
            except Exception:
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                return val

        return self.__default_float

    def get_int(self, value: str) -> int:
        """
            If the value exists, return the integer
            corresponding to the string.

            If it does not exist, or the value cannot be converted to an integer,
            return the default integer.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value)

            try:
                val = int(val)
            except Exception:
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                return val

        return self.__default_int

    def get_str(self, value: str) -> str:
        """
            If the value exists, return the string,
            otherwise return the default string.
        """
        if self.check_value(value):
            return self.__config.get(self.__section, value)

        return self.__default_string

    def get_list(self, value: str) -> list:
        """
            If the value exists, return a list.,
            If it does not exist, or it cannot be converted to a list, return the default list.
        """
        if self.check_value(value):
            value = self.__config.get(self.__section, value)
            try:
                values = ast.literal_eval(value)
            except Exception:
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                return values

        return deepcopy(self.__default_list)

    def get_bool_defval(self, value: str, default: bool) -> bool:
        """
            If the value exists, return the boolean
            corresponding to the string.

            If it does not exist, or the value cannot be converted to a boolean,
            return the second argument.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value).lower()

            if val in self.__accepted_false_bool:
                return False

            elif val in self.__accepted_true_bool:
                return True

        return default

    def get_float_defval(self, value: str, default: float) -> float:
        """
            If the value exists, return the float
            corresponding to the string.

            If it exists, or the value cannot be converted to a float,
            return the second argument.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value)
            try:
                val = float(val)
            except Exception:
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                return val

        return default

    def get_int_defval(self, value: str, default: int) -> int:
        """
            If the value exists, return the integer
            corresponding to the string.

            If it exists, or the value cannot be converted to an integer,
            return the second argument.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value)
            try:
                val = int(val)
            except Exception:
                if self.__print_errors:
                    print(traceback.format_exc())
            else:
                return val

        return default

    def get_str_defval(self, value: str, default: str) -> str:
        """
            If the value exists, return the string,
            if it does not exist, return the second argument.
        """
        if self.check_value(value):
            return self.__config.get(self.__section, value)

        return default

    def get_default_bool(self) -> bool:
        return self.__default_bool

    def get_default_float(self) -> float:
        return self.__default_float

    def get_default_str(self) -> str:
        return self.__default_string

    def get_default_int(self) -> int:
        return self.__default_int

    def get_default_list(self) -> list:
        return deepcopy(self.__default_list)

    def get_section(self) -> str:
        return self.__section

    def get_configuration_path(self) -> str:
        return self.__ini_path

    def set_configuration_path(self, ini_path: str) -> None:
        """Set the path to the configuration file."""
        if isinstance(ini_path, str):
            self.__ini_path = ini_path
            if not os.path.exists(ini_path):
                print("CCParser Warning: the path to the configuration file does not exists")
        else:
            print("CCParser Warning: The path is not valid.\n")
            self.__ini_path = ''
        print(ini_path)

    def set_section(self, section: str) -> None:
        """
            Set the section to check for values.
        """
        self.__section = section

    def set_default_float(self, value: float) -> None:
        """
            Set the default float to return when a value does not exist.
            By default, it returns 0.0
        """
        self.__default_float = value

    def set_default_string(self, value: str) -> None:
        """
            Set the default string to return when a value does not exist.
            By default, it returns an empty string.
        """
        self.__default_string = value

    def set_default_bool(self, value: bool) -> None:
        """
            Set the default boolean to return when a value does not exist.
            By default, it returns false
        """
        self.__default_bool = value

    def set_default_int(self, value: int) -> None:
        """
            Set the default integer to return when a value does not exist.
            By default, it returns 0
        """
        self.__default_int = value

    def set_default_list(self, value: list) -> None:
        """
            Set the default integer to return when a value does not exist.
            By default, it returns 0
        """
        self.__default_list = deepcopy(value)
