#!/usr/bin/env python
# -*- coding: utf8 -*-

import AvivoreXT
from AvivoreXT import Avivore, AvivoreError, AvivoreConfig, QueryThread
import sys
import time


query_thread = None


def main(argv, test_running=False):
    """
    Avivore main() function.

    :param argv:    Array containing command line arguments.
    :return:        None
    """
    # create AvivoreConfig instance
    if '-c' == argv[1]:
        config = AvivoreConfig.AvivoreConfig(0, argv[2])
    elif '-d' == argv[1]:
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

    # enter main processing loops if not in testing mode
    if not test_running:
        main_loop(query_thread, avivore)


def main_loop(query_thread_inst, avivore_inst):
    query_thread_inst.start()

    time.sleep(1)

    # continue with twitter stream monitoring
    avivore_inst.twitter_stream_main()


def software_init_msg(version):
    """
    Prints AvivoreXT welcome message.

    :param version: Version number of AvivoreXT release.
    :return:        None
    """
    print('AvivoreXT ' + version + ' by rc0r (https://github.com/rc0r)')


def software_exit(status, message):
    """
    Exit function, prints exit message and quits AvivoreXT with a user provided status code.

    :param status:  Exit status code.
    :param message: Message to display.
    :return:        None
    """
    print('')
    print('%s' % message)
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
        if argv[1] != '-c' and argv[1] != '-d':
            print_usage = True

    if print_usage:
        print('Usage: %s -c <config-file>|-d <config-dbfile>' % argv[0])
        raise AvivoreError.AvivoreError('Check usage!')


def start(test_running=False):
    """
    AvivoreXT start procedure.

    :return:    None
    """
    software_init_msg(AvivoreXT.__version__)
    try:
        check_usage(sys.argv)
        main(sys.argv, test_running)
    except KeyboardInterrupt:
        software_exit(0, 'Exiting the application.')
    except AvivoreError.AvivoreError:
        software_exit(0, 'Try again!')
    except:
        main(sys.argv, test_running)
        raise


if __name__ == '__main__':
    start()
