# -*- coding: utf8 -*-
import time
import sys

"""
Helper functions
"""


def is_sequence(arg):
    # check if arg is list, tuple, ...
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))


def output(string):
    # Default text output for the console.
    if isinstance(string, str):
        # This is sort of lame but whatever:
        print("[" + str(round(time.time(), 0))[:-2] + "] " + string)


