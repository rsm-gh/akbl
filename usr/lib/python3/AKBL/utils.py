#!/usr/bin/python3
#

#
# Public domain.
#
#
# gtk_utils.py by Rafael Senties Martinelli.
#
# To the extent possible under law, the person who associated CC0 with
# gtk_utils.py has waived all copyright and related or neighboring rights
# to gtk_utils.py.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <https://creativecommons.org/publicdomain/zero/1.0/>.


import os
import re
import pwd



def getuser() -> str:
    return pwd.getpwuid(os.geteuid()).pw_name


def rgb_to_hex(rgb) -> str:
    return '#%02x%02x%02x' % (int(rgb[0]), int(rgb[1]), int(rgb[2]))


def string_is_hex_color(string) -> bool:
    if isinstance(string, str) and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', string):
        return True

    return False
