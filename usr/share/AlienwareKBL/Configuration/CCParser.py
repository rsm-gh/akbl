#!/usr/bin/python3

#  Copyright (C) 2014-2016  Rafael Senties Martinelli 
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

"""
    To allow the compatibility with python2.7, `with open()` can not use
    encoding='utf-8'.  Anyways the default encoding is utf-8.
"""

try:
    import ConfigParser as configparser  # python2
except:
    import configparser  # python3

import os
import traceback

__version__ = '1.4.8~4'


class CCParser(object):

    def __init__(self, ini_path='', section='', debug=False):
        """
            To init CCParser you can enter a path
            and a section. If you doesn't know them yet
            you can leave them empty.

            If debug is set to True, all the exceptions
            will print its traceback.
        """
        self._debug = debug

        self._config = configparser.ConfigParser()

        if ini_path != '':
            self.set_configuration_path(ini_path)

        if section != '':
            self.set_section(section)

        self._default_bool = False
        self._default_string = ''
        self._default_int = 0
        self._default_float = 0.0

        self._accepted_true_bool = ['true', 'yes']  # must be lower case
        self._accepted_false_bool = ['false', 'no']  # must be lower case

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
'''.format( self.get_configuration_path(),
            self.get_section(),
            self.get_default_bool(),
            self.get_default_float(),
            self.get_default_int(),
            self.get_default_str()
            ))

    def check_value(self, value):
        """
            return False if the value don't exists,
            return True if the value exists
        """
        if not os.path.exists(self.ini_path):
            return False
        else:
            try:
                self._config.read(self.ini_path)
            except Exception as e:
                print("CCParser Warning: reading damaged file or file without section")
                print(traceback.format_exc())
                print()
                return False

            if not self._config.has_section(self._section):
                return False
            elif self._config.has_option(self._section, value):
                return True
            else:
                return False

    def get_bool(self, value):
        """
            If the value exists, return the boolean
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a boolean, return the default boolean.
        """

        if self.check_value(value):
            val = self._config.get(self._section, value).lower()
            if val in self._accepted_false_bool:
                return False
            elif val in self._accepted_true_bool:
                return True
            else:
                return self._default_bool
        else:
            return self._default_bool

    def get_float(self, value):
        """
            If the value exists, return the float
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a float, return the default float.
        """
        if self.check_value(value):
            val = self._config.get(self._section, value)
            try:
                val = float(val)
                return val
            except Exception as e:
                if self._debug:
                    print(traceback.format_exc())

                return self._default_float
        else:
            return self._default_float

    def get_int(self, value):
        """
            If the value exists, return the integer
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a integer, return the default integer.
        """
        if self.check_value(value):
            val = self._config.get(self._section, value)

            try:
                val = int(val)
                return val
            except Exception as e:
                if self._debug:
                    print(traceback.format_exc())

                return self._default_int
        else:
            return self._default_int

    def get_str(self, value):
        """
            If the value exists, return the string,
            other wise return the default string.
        """
        if self.check_value(value):
            return self._config.get(self._section, value)
        else:
            return self._default_string

    def get_bool_defval(self, value, default):
        """
            If the value exists, return the boolean
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a boolean, return the the second argument.
        """
        if self.check_value(value):
            val = self._config.get(self._section, value).lower()

            if val in self._accepted_false_bool:
                return False
            elif val in self._accepted_true_bool:
                return True
            else:
                return default
        else:
            return default

    def get_float_defval(self, value, default):
        """
            If the value exists, return the float
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a float, return the the second argument.
        """
        if self.check_value(value):
            val = self._config.get(self._section, value)
            try:
                val = float(val)
                return val
            except Exception as e:
                if self._debug:
                    print(traceback.format_exc())

                return default
        else:
            return default

    def get_int_defval(self, value, default):
        """
            If the value exists, return the integer
            corresponding to the string. If it does
            not exists, or the value can not be converted
            to a integer, return the the second argument.
        """
        if self.check_value(value):
            val = self._config.get(self._section, value)
            try:
                val = int(val)
                return val
            except Exception as e:
                if self._debug:
                    print(traceback.format_exc())

                return default
        else:
            return default

    def get_str_defval(self, value, default):
        """
            If the value exists, return the string,
            if it does not exists, return the the
            second argument.
        """
        if self.check_value(value):
            return self._config.get(self._section, value)
        else:
            return default

    def set_configuration_path(self, ini_path):
        """
            Set the path to the configuration file.
        """
        if isinstance(ini_path, str):
            self.ini_path = ini_path
            if not os.path.exists(ini_path) and self._debug:
                print("CCParser Warning: the path to the configuration file does not exists\n")
        else:
            print("CCParser Warning: The path is not valid.\n")
            self.ini_path = ''

    def set_section(self, section):
        """
            Set the section to check for values.
        """
        section = str(section)
        self._section = section

    def set_default_float(self, float):
        """
            Set the default float to return when
            a value does not exists. By default
            it returns 0.0
        """
        self._default_float = float

    def set_default_string(self, str):
        """
            Set the default string to return when
            a value does not exists. By default
            it returns an empty string.
        """

        self._default_string = str

    def set_default_bool(self, bool):
        """
            Set the default boolean to return when
            a value does not exists. By default
            it returns false
        """
        self._default_bool = bool

    def set_default_int(self, int):
        """
            Set the default integer to return when
            a value does not exists. By default
            it returns 0
        """
        self._default_int = int

    def write(self, value_name, value):
        """
            Write the value name and its value.

            If the config file does not exists,
            or the directories to the path, they
            will be created.
        """

        if self.ini_path != '' and isinstance(self.ini_path, str):

            if not os.path.exists(os.path.dirname(self.ini_path)):
                os.makedirs(os.path.dirname(self.ini_path))

            if not os.path.exists(self.ini_path):
                open(self.ini_path, 'wt').close()

            try:
                self._config.read(self.ini_path)
            except Exception as e:
                print("CCParser Warning: reading damaged file or file without section")
                print(traceback.format_exc())
                print()
                return False

            if not self._config.has_section(self._section):
                self._config.add_section(self._section)

            self._config.set(self._section, value_name, str(value))

            with open(self.ini_path, 'w') as f:
                self._config.write(f)
        else:
            print(
                "CCParser Error: Trying to write the configuration without an ini path.")
            print("Configuration Path: " + str(self.get_configuration_path()))
            print()

    def get_default_bool(self):
        return self._default_bool

    def get_default_float(self):
        return self._default_float

    def get_default_str(self):
        return self._default_string

    def get_default_int(self):
        return self._default_int

    def get_section(self):
        return self._section

    def get_configuration_path(self):
        return self.ini_path

if __name__ == '__main__':
    """
        This is for testing purposes.
    """

    path = '/home/rsm/Desktop/test.ini'  # unexisting file

    if os.path.exists(path):
        os.remove(path)

    cp = CCParser(path, 'test')

    print('section:', cp.get_section())
    cp.write('bool', False)
    print(cp.get_bool('bool'))
    cp.write('bool', True)
    print(cp.get_bool('bool'))

    cp.write('string1', 'this is a test')
    print(cp.get_str('string1'))

    cp.print_info()
