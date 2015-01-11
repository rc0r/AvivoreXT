#!/usr/bin/env python
# -*- coding: utf8 -*-

import AvivoreXT
from AvivoreXT import Avivore, AvivoreConfig, QueryThread
import sys
import time


query_thread = None


def main(argv):
    """
    Avivore main() function.

    :param argv:    Array containing command line arguments.
    :return:        None
    """
    # create AvivoreConfig instance
    if "-c" == argv[1]:
        config = AvivoreConfig.AvivoreConfig(0, argv[2])
    elif "-d" == argv[1]:
        config = AvivoreConfig.AvivoreConfig(1, argv[2])
    else:
        return -1

    # read & parse config file
    config.read_config()

    # prepare database
    config.init_database()

    # create Avivore instance
    avivore = Avivore.Avivore(config)

    # spawn twitter search query thread
    global query_thread
    query_thread = QueryThread.QueryThread(avivore)
    query_thread.setDaemon(True)
    query_thread.start()

    time.sleep(1)

    # continue with twitter stream monitoring
    avivore.twitter_stream_main()


def software_init_msg(version):
    """
    Prints AvivoreXT welcome message.

    :param version: Version number of AvivoreXT release.
    :return:        None
    """
    print("AvivoreXT " + version + " by rc0r (https://github.com/rc0r)")


def software_exit(status, message):
    """
    Exit function, prints exit message and quits AvivoreXT with a user provided status code.

    :param status:  Exit status code.
    :param message: Message to display.
    :return:        None
    """
    print("")
    print(message)
    sys.exit(status)


def check_usage(argv):
    """
    Checks for correct program invocation from the command line and prints usage information if necessary.

    :param argv:    Array containing all command line arguments passed to AvivoreXT
    :return:        None
    """
    print_usage = False
    if 3 != len(argv):
        print_usage = True
    else:
        if argv[1] != "-c" and argv[1] != "-d":
            print_usage = True

    if print_usage:
        print("Usage: %s -c <config-file>|-d <config-dbfile>" % argv[0])
        sys.exit(-1)


def start():
    """
    AvivoreXT start procedure.

    :return:    None
    """
    software_init_msg(AvivoreXT.__version__)
    check_usage(sys.argv)
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        software_exit(0, "Exiting the application.")
    except:
        main(sys.argv)
        raise


if __name__ == "__main__":
    start()
