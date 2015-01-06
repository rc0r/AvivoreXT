# -*- coding: utf-8 -*-

import unittest
import os
from AvivoreXT import Compat, AvivoreConfig
import sqlite3 as lite
from sqlite3 import DatabaseError

if Compat.is_python3():
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


class AvivoreConfigTestCase(unittest.TestCase):
    def setUp(self):
        # code to execute in preparation for tests
        os.symlink('../sample.conf', './testdata/test.conf')
        os.symlink('../sample_conf.db', './testdata/test.db')

    def tearDown(self):
        # code to execute to clean up after tests
        os.remove('./testdata/test.conf')
        os.remove('./testdata/test.db')

    def test_read_config(self):
        config_files = [
            './testdata/test.conf',
            './testdata/invalid.conf',
            './testdata/test.db',
            './testdata/empty_config.db',
            './testdata/empty_typedefs.db',
            './testdata/invalid_config.db',
            './testdata/not_exists.db',
            './invalidpath/invalidfile',
            123,
            123.45,
            None,
            True,
        ]

        for i in range(0, 10, 1):
            for j in range(0, len(config_files), 1):
                if j < 8:
                    avivore_conf_inst = AvivoreConfig.AvivoreConfig(i, config_files[j])
                    self.assertIsInstance(avivore_conf_inst, AvivoreConfig.AvivoreConfig)

                    # test init
                    self.assertTrue(avivore_conf_inst.config_type == i)
                    self.assertTrue(avivore_conf_inst.config_filename == config_files[j])
                    self.assertTrue(isinstance(avivore_conf_inst.config, ConfigParser))
                    self.assertTrue(avivore_conf_inst.twitter_search_types == [])
                    self.assertTrue(avivore_conf_inst.twitter_search_terms == [])
                    self.assertTrue(avivore_conf_inst.twitter_track_keywords is None)
                    self.assertTrue(avivore_conf_inst.twitter_consumer_key is None)
                    self.assertTrue(avivore_conf_inst.twitter_consumer_secret is None)
                    self.assertTrue(avivore_conf_inst.twitter_search_interval == 30)
                    self.assertTrue(avivore_conf_inst.credentials_file is None)
                    self.assertTrue(avivore_conf_inst.database_path is None)
                    self.assertEqual(avivore_conf_inst.mandatory_options,
                                     [('database', 'dbpath'),
                                      ('twitter_auth', 'consumer_key'),
                                      ('twitter_auth', 'consumer_secret'),
                                      ('twitter_auth', 'credentials_file'),
                                      ('twitter_search', 'stream_tracking_keyword'),
                                      ('twitter_search', 'csv_search_term'),
                                      ('twitter_search_objects', '0')])
                else:
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        avivore_conf_inst = AvivoreConfig.AvivoreConfig(i, config_files[j])
                        self.assertIsInstance(avivore_conf_inst, AvivoreConfig.AvivoreConfig)

                #print(i, j)  # debug

                if (i == 0 and j == 0) or (i == 1 and j == 2):
                    # read from valid config file OR read from valid database
                    self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 0 and j == 1:
                    # read from incomplete config file
                    with self.assertRaises(AvivoreConfig.MissingConfigItemException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 0 and (j == 2 or j == 3 or j == 4 or j == 5):
                    # read from corrupt (binary) config file
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 0 and j > 5:
                    # read from non-existent config file
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 1 and (j == 0 or j == 1):
                    # read from corrupt database file
                    with self.assertRaises(DatabaseError):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 1 and j == 3:
                    # read from empty database
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 1 and j == 4:
                    # read from database with empty typedefs table
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 1 and j == 5:
                    # read from database with invalid config
                    with self.assertRaises(AvivoreConfig.MissingConfigItemException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                elif i == 1 and j == 6:
                    # create new config database
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                    os.remove('./testdata/not_exists.db')
                elif i == 1 and j > 6:
                    # read/create database file at non-existent location
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())
                else:
                    with self.assertRaises(AvivoreConfig.AvivoreConfigException):
                        self.assertIsNone(avivore_conf_inst.read_config())

    def test_init_database(self):
        avivore_conf_inst = AvivoreConfig.AvivoreConfig(0, './testdata/test.conf')

        self.assertIsInstance(avivore_conf_inst, AvivoreConfig.AvivoreConfig)

        # check with database path of wrong type
        avivore_conf_inst.database_path = None
        with self.assertRaises(AvivoreConfig.AvivoreConfigException):
            self.assertIsNone(avivore_conf_inst.init_database())

        # check with non-existent database
        avivore_conf_inst.database_path = './testdata/data.db'
        self.assertIsNone(avivore_conf_inst.init_database())
        os.remove('./testdata/data.db')

        # check with existent database but without data table
        avivore_conf_inst.database_path = './testdata/empty_typedefs.db'
        self.assertIsNone(avivore_conf_inst.init_database())
        dbcon = lite.connect(avivore_conf_inst.database_path)
        dbcur = dbcon.cursor()
        dbcur.execute('DROP TABLE Data')

        # check with existent database with data table
        avivore_conf_inst.database_path = './testdata/empty_config.db'
        self.assertIsNone(avivore_conf_inst.init_database())


def test_main():
    unittest.main()


if __name__ == '__main__':
    test_main()
