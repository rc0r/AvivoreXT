# -*- coding: utf-8 -*-

import unittest
from AvivoreXT import Avivore, QueryThread, AvivoreError
import os
import shutil


class QueryThreadTestCase(unittest.TestCase):
    def setUp(self):
        # code to execute in preparation for tests
        shutil.copyfile('./sample_conf.db', './testdata/test.db')

        self.avivore_conf = Avivore.AvivoreConfig.AvivoreConfig(1, './testdata/test.db')
        self.avivore_conf.read_config()
        self.avivore_conf.init_database()
        self.avivore_conf.twitter_search_interval = 0
        self.avivore = Avivore.Avivore(self.avivore_conf)
        self.query_thread_instance = QueryThread.QueryThread(self.avivore)

    def tearDown(self):
        # code to execute to clean up after tests
        os.remove('./testdata/test.db')

    def test_run_init(self):
        # test for network failure or twitter authentication error (no valid twitter credentials in config file)
        with self.assertRaises(AvivoreError.TwitterAuthenticationException):
            self.assertIsNone(self.query_thread_instance.init_run())

    @unittest.skip('This test assumes there are valid twitter credentials in sample_conf.db!')
    def test_run_init_working_creds(self):
        # test in case network is working
        self.assertIsNone(self.query_thread_instance.init_run())

    def test_twitter_search(self):
        self.assertIsNone(self.query_thread_instance.twitter_search(self.avivore))

    def test_extract_data_from_tweet(self):
        tweet = {
            'id': '0123456789',
            'created_at': '000000000',
            'user': {
                'id_str': '987654321',
                'screen_name': '_rc0r',
            },
            'text': 'This is a test tweet! My server ip: 10.11.12.13!',
        }

        # process unseen tweet
        self.assertIsNone(self.query_thread_instance.extract_data_from_tweet(self.avivore, tweet))
        # process dupe
        self.assertIsNone(self.query_thread_instance.extract_data_from_tweet(self.avivore, tweet))


def test_main():
    unittest.main()


if __name__ == '__main__':
    test_main()
