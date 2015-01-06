# -*- coding: utf8 -*-
import sys


def is_python3():
    """
    Check if interpreter is Python 3.

    :return:    True if interpreter is Python 3, False otherwise.
    """
    return sys.version_info[0] == 3
