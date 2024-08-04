#!/usr/bin/python3

#
# MIT License
#
#  Copyright (C) 2018, 2024 Rafael Senties Martinelli.
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
import inspect
from datetime import datetime

_RED = "\033[1;31m"
_BLUE = "\033[1;34m"
_CYAN = "\033[1;36m"
_GREEN = "\033[0;32m"
_RESET = "\033[0;0m"
_LIGHT_YELLOW = "\033[0;93m"

__version__ = "1.0"


class DebugCodes:
    _error = 0
    _warning = 1
    _info = 2
    _debug = 3


if 'DEBUG' in os.environ:
    match os.environ['DEBUG'].lower():
        case "error":
            _DEBUG = DebugCodes._error
        case "warning":
            _DEBUG = DebugCodes._warning
        case "info":
            _DEBUG = DebugCodes._info
        case "debug":
            _DEBUG = DebugCodes._debug
        case _:
            _DEBUG = DebugCodes._warning
else:
    _DEBUG = DebugCodes._warning


def print_error(message, direct_output=False):
    if direct_output:
        print(message, flush=True)
        return

    isp1 = inspect.stack()[1]
    module_name = __parse_module_name(inspect.getmodule(isp1[0]))
    method_name = isp1[3]

    print('\n{}{} [ERROR]: "{}" {}{}:\n{}'.format(_RED,
                                                  __datetime_str(),
                                                  module_name,
                                                  method_name,
                                                  _RESET,
                                                  str(message).strip()), flush=True)


def print_warning(message, direct_output=False):
    if _DEBUG < DebugCodes._warning:
        return

    if direct_output:
        print(message, flush=True)
        return

    isp1 = inspect.stack()[1]
    module_name = __parse_module_name(inspect.getmodule(isp1[0]))
    method_name = isp1[3]

    print('\n{}{} [WARNING]: "{}" {}:{}\n{}'.format(_LIGHT_YELLOW,
                                                    __datetime_str(),
                                                    module_name,
                                                    method_name,
                                                    _RESET,
                                                    str(message).strip()), flush=True)


def print_info(message, direct_output=False):
    if _DEBUG < DebugCodes._info:
        return

    if direct_output:
        print(message, flush=True)
        return

    isp1 = inspect.stack()[1]
    module_name = __parse_module_name(inspect.getmodule(isp1[0]))
    method_name = isp1[3]

    print('\n{}{} [INFO]: "{}" {}{}:\n{}'.format(_GREEN,
                                                 __datetime_str(),
                                                 module_name,
                                                 method_name,
                                                 _RESET,
                                                 str(message).strip()), flush=True)


def print_debug(message=None, direct_output=False):
    if _DEBUG < DebugCodes._debug:
        return

    if direct_output:
        print(message, flush=True)
        return

    isp1 = inspect.stack()[1]
    module_name = __parse_module_name(inspect.getmodule(isp1[0]))
    method_name = isp1[3]

    if message is None:
        print('\n{}{} [DEBUG]: "{}" {}{}'.format(_CYAN,
                                                 __datetime_str(),
                                                 module_name,
                                                 method_name,
                                                 _RESET), flush=True)
    else:
        print('\n{}{} [DEBUG]: "{}" {}:{}\n{}'.format(_CYAN,
                                                      __datetime_str(),
                                                      module_name,
                                                      method_name,
                                                      _RESET,
                                                      str(message).strip()), flush=True)


def __datetime_str():
    return str(datetime.now()).split(".")[0]


def __parse_module_name(name):
    return str(name).split("from '", 1)[1].split("'>", 1)[0]


if __name__ == '__main__':
    _DEBUG = DebugCodes._debug
    print_error('this is an error!')
    print_warning('this is a warning!')
    print_info("this is an info!")
    print_debug('this is a DEBUG message!')
