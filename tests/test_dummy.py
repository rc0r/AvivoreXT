# -*- coding: utf-8 -*-

import unittest
from test import test_support


class DummyTestCase(unittest.TestCase):
    # def setUp(self):
    #     # code to execute in preparation for tests
    #     pass
    #
    # def tearDown(self):
    #     # code to execute to clean up after tests
    #     pass
    def test_feature_dummy(self):
        self.failUnless(True)


def test_main():
    test_support.run_unittest(DummyTestCase)

if __name__ == '__main__':
    test_main()