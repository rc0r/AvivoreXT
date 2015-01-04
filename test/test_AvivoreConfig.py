# -*- coding: utf-8 -*-

import unittest
#from test import test_support
from AvivoreXT import Compat, AvivoreConfig

if Compat.is_python3():
    from configparser import ConfigParser
else:
    from ConfigParser import ConfigParser


class AvivoreConfigTestCase(unittest.TestCase):
    # def setUp(self):
    #     # code to execute in preparation for tests
    #     pass
    #
    # def tearDown(self):
    #     # code to execute to clean up after tests
    #     pass
    def test_init(self):
        config_files = [
            'testdata/test.conf',
            'testdata/test.db',
            'invalidpath/invalidfile',
        ]

        for i in range(0, 10, 1):
            for j in range(0, len(config_files), 1):
                avivore_conf_inst = AvivoreConfig.AvivoreConfig(i, config_files[j])
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

    def test_read_config(self):
        pass

    def test_init_config_database(self):
        pass

    def test_init_database(self):
        pass


def test_main():
    #test_support.run_unittest(AvivoreConfigTestCase)
    #suite = unittest.defaultTestLoader.loadTestsFromTestCase(AvivoreConfigTestCase)
    #unittest.TextTestRunner().run(suite)
    #unittest.main()

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tcl = loader.loadTestsFromTestCase

    testClasses = [
        'AvivoreConfigTestCase'
    ]

    for c in testClasses:
        suite.addTest(tcl(c))

    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    test_main()
