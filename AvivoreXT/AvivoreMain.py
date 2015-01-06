#!/usr/bin/env python
# -*- coding: utf8 -*-

import AvivoreXT
from AvivoreXT import Avivore, AvivoreConfig, QueryThread
import sys
import time


query_thread = None


def main(argv):
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
    print("AvivoreXT " + version + " by rc0r (https://github.com/rc0r)")


def software_exit(status, message):
    print("")
    print(message)
    sys.exit(status)


def check_usage(argv):
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
