# -*- coding: utf8 -*-
import time

"""
Helper functions
"""


def is_string(arg):
    try:
        obj = basestring
    except NameError:
        obj = str

    return isinstance(arg, obj)


def is_sequence(arg):
    # check if arg is list, tuple, ...
    return (not is_string(arg) and
            (hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__")))


def output(string):
    # Default text output for the console.
    if isinstance(string, str):
        # This is sort of lame but whatever:
        print("[" + str(round(time.time(), 0))[:-2] + "] " + string)


