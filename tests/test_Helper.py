# -*- coding: utf-8 -*-

from AvivoreXT import Helper
import unittest
from test import test_support
from array import array


class HelperTestCase(unittest.TestCase):
    # def setUp(self):
    #     # code to execute in preparation for tests
    #     pass
    #
    # def tearDown(self):
    #     # code to execute to clean up after tests
    #     pass
    def test_is_sequence(self):
        # testing sequential types
        self.assertTrue(Helper.is_sequence("Hello World"))
        self.assertTrue(Helper.is_sequence(['value1', 'value2', 'value3']))
        self.assertTrue(Helper.is_sequence(('item1', 'item2')))
        self.assertTrue(Helper.is_sequence('c'))
        self.assertTrue(Helper.is_sequence(array('l', [1, 2, 3, 4, 5])))
        self.assertTrue(Helper.is_sequence(array('d', [1.0, 2.0, 3.0, 4.0, 5.0])))
        self.assertTrue(Helper.is_sequence(bytearray.fromhex("deadbeef")))
        self.assertTrue(Helper.is_sequence(dict(one=1, two=2, three=3)))

        # testing non-sequential types
        self.assertFalse(Helper.is_sequence(3))
        self.assertFalse(Helper.is_sequence(3.14))
        self.assertFalse(Helper.is_sequence(self))
        self.assertFalse(Helper.is_sequence(None))
        self.assertFalse(Helper.is_sequence(True))
        self.assertFalse(Helper.is_sequence(Helper.is_sequence))

    def test_output(self):
        self.assertIsNone(Helper.output("Test"))
        self.assertIsNone(Helper.output(u"\u2031\u203c\u2049"))
        self.assertIsNone(Helper.output(self))
        self.assertIsNone(Helper.output(None))
        self.assertIsNone(Helper.output(True))
        self.assertIsNone(Helper.output(Helper.output))
        self.assertIsNone(Helper.output(3))
        self.assertIsNone(Helper.output(3.14))
        self.assertIsNone(Helper.output(['a1', 'b2', 'c3']))
        self.assertIsNone(Helper.output(('it1', 'it2')))
        self.assertIsNone(Helper.output(array('l', [1, 2, 3, 4, 5])))
        self.assertIsNone(Helper.output(array('B', [0x41, 0x42, 0x43, 0x44, 0x45])))
        self.assertIsNone(Helper.output(bytearray.fromhex("deadbeef")))
        self.assertIsNone(Helper.output(dict(one=1, two=2, three=3)))


def test_main():
    test_support.run_unittest(HelperTestCase)

if __name__ == '__main__':
    test_main()