#!/usr/bin/python3

#
# MIT License
#
# Copyright (c) 2014-2016, 2024 Rafael Senties Martinelli.
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
import traceback
import configparser

__version__ = '0.6.4'


class CCParser(object):

    def __init__(self, ini_path='', section='', debug=False):
        """
            To init CCParser you can enter a path and a section.
            If you don't know them, you can leave them empty.

            If debug is set to True, all the exceptions
            will print its traceback.
        """
        self.__debug = debug
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

        self.__accepted_true_bool = ['true', 'yes']
        self.__accepted_false_bool = ['false', 'no']

        self.__version__ = __version__

    def print_info(self):
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

    def check_value(self, value):
        """
            return False if the value does not exist.
            return True if the value exists.
        """
        if os.path.exists(self.__ini_path):
            try:
                self.__config.read(self.__ini_path)
            except Exception:
                print("CCParser Warning: reading damaged file or file without section")
                if self.__debug:
                    print(traceback.format_exc())
            else:
                if self.__config.has_section(self.__section) and self.__config.has_option(self.__section, value):
                    return True

        return False

    def write(self, value_name, value):
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
                return False

            if not self.__config.has_section(self.__section):
                self.__config.add_section(self.__section)

            self.__config.set(self.__section, value_name, str(value))

            with open(self.__ini_path, 'w') as f:
                self.__config.write(f)
        else:
            print("CCParser Error: Trying to write the configuration without an ini path.")
            print("Configuration Path: " + str(self.get_configuration_path()))
            print()

    def get_bool(self, value):
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

    def get_float(self, value):
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
                if self.__debug:
                    print(traceback.format_exc())
            else:
                return val

        return self.__default_float

    def get_int(self, value):
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
                if self.__debug:
                    print(traceback.format_exc())
            else:
                return val

        return self.__default_int

    def get_str(self, value):
        """
            If the value exists, return the string,
            otherwise return the default string.
        """
        if self.check_value(value):
            return self.__config.get(self.__section, value)

        return self.__default_string

    def get_list(self, value):
        """
            If the value exists, return the integer corresponding to the string,
            If it does not exist, or it cannot be converted to an integer, return the default integer.
        """
        if self.check_value(value):
            val = self.__config.get(self.__section, value)

            try:
                val = val.split("|")
            except Exception:
                if self.__debug:
                    print(traceback.format_exc())
            else:
                return val

        return self.__default_list

    def get_bool_defval(self, value, default):
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

    def get_float_defval(self, value, default):
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
                if self.__debug:
                    print(traceback.format_exc())
            else:
                return val

        return default

    def get_int_defval(self, value, default):
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
                if self.__debug:
                    print(traceback.format_exc())
            else:
                return val

        return default

    def get_str_defval(self, value, default):
        """
            If the value exists, return the string,
            if it does not exist, return the second argument.
        """
        if self.check_value(value):
            return self.__config.get(self.__section, value)

        return default

    def get_default_bool(self):
        return self.__default_bool

    def get_default_float(self):
        return self.__default_float

    def get_default_str(self):
        return self.__default_string

    def get_default_int(self):
        return self.__default_int

    def get_default_list(self):
        return self.__default_list

    def get_section(self):
        return self.__section

    def get_configuration_path(self):
        return self.__ini_path

    def set_configuration_path(self, ini_path):
        """Set the path to the configuration file."""
        if isinstance(ini_path, str):
            self.__ini_path = ini_path
            if not os.path.exists(ini_path):
                print("CCParser Warning: the path to the configuration file does not exists")
        else:
            print("CCParser Warning: The path is not valid.\n")
            self.__ini_path = ''
        print(ini_path)

    def set_section(self, section):
        """
            Set the section to check for values.
        """
        section = str(section)
        self.__section = section

    def set_default_float(self, float_value):
        """
            Set the default float to return when a value does not exist.
            By default, it returns 0.0
        """
        self.__default_float = float_value

    def set_default_string(self, str_value):
        """
            Set the default string to return when a value does not exist.
            By default, it returns an empty string.
        """

        self.__default_string = str_value

    def set_default_bool(self, bool_value):
        """
            Set the default boolean to return when a value does not exist.
            By default, it returns false
        """
        self.__default_bool = bool_value

    def set_default_int(self, int_value):
        """
            Set the default integer to return when a value does not exist.
            By default, it returns 0
        """
        self.__default_int = int_value

    def set_default_list(self, value):
        """
            Set the default integer to return when a value does not exist.
            By default, it returns 0
        """
        self.__default_list = value
