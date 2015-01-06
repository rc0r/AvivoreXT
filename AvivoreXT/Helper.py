# -*- coding: utf8 -*-
import os
import time

"""
Helper functions
"""


def is_string(arg):
    """
    Tests if argument is instance of a string type.

    :param arg: Variable to be tested
    :return: True if :arg is a string, False otherwise.
    """
    try:
        obj = basestring
    except NameError:
        obj = str

    return isinstance(arg, obj)


def is_sequence(arg):
    """
    Checks if an object is sequential type (like list, tuple, ...), but not a string.

    :param arg: Object under test.
    :return:    True if object is sequential type (and not string), False otherwise.
    """
    return (not is_string(arg) and
            (hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__")))


def filepath_exists(filename):
    """
    Test if path to a given file exists. Specified file itself must not exist. If you want to test a directory itself
    make sure to append a final separator, f.e. '/' on unix-like systems!

    :param filename:    Filename containing full relative or absolute path, or path name with trailing separator
    :return:            True if path exists, False otherwise. Note: filepath_exists() does not check whether the
                        specified file itself exists!
    """
    # TODO:
    #   - test on windows
    #   - if necessary, make platform independent
    separator = '/'
    #if sys.platform.startswith('win'):
    #    separator = '\\'

    ret = False
    if is_string(filename):
        pos = str.rfind(filename, separator)
        if pos > 0:
            pathname = filename[:str.rfind(filename, separator)]
        elif pos == 0:
            pathname = separator
        else:
            pathname = filename

        if os.path.exists(pathname):
            ret = True
    return ret


def output(string):
    """
    Prints a unix timestamp followed by a provided message.

    :param string:  The message to print
    :return:        None
    """
    # Default text output for the console.
    if is_string(string):
        # This is sort of lame but whatever:
        print("[" + str(round(time.time(), 0))[:-2] + "] " + string)
