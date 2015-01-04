# -*- coding: utf-8 -*-

import unittest
#from test import test_support
from array import array
from AvivoreXT import Helper


class HelperTestCase(unittest.TestCase):
    # def setUp(self):
    #     # code to execute in preparation for tests
    #     pass
    #
    # def tearDown(self):
    #     # code to execute to clean up after tests
    #     pass
    def test_is_string(self):
        # testing non-string types
        self.assertFalse(Helper.is_string(['value1', 'value2', 'value3']))
        self.assertFalse(Helper.is_string(('item1', 'item2')))
        self.assertFalse(Helper.is_string(array('l', [1, 2, 3, 4, 5])))
        self.assertFalse(Helper.is_string(array('d', [1.0, 2.0, 3.0, 4.0, 5.0])))
        self.assertFalse(Helper.is_string(bytearray.fromhex("deadbeef")))
        self.assertFalse(Helper.is_string(dict(one=1, two=2, three=3)))
        self.assertFalse(Helper.is_string(3))
        self.assertFalse(Helper.is_string(3.14))
        self.assertFalse(Helper.is_string(self))
        self.assertFalse(Helper.is_string(None))
        self.assertFalse(Helper.is_string(True))
        self.assertFalse(Helper.is_string(Helper.is_string))

        # testing string types
        self.assertTrue(Helper.is_string("Hello World"))
        self.assertTrue(Helper.is_string("Hello World\u203c"))

    def test_is_sequence(self):
        # testing sequential types
        self.assertTrue(Helper.is_sequence(['value1', 'value2', 'value3']))
        self.assertTrue(Helper.is_sequence(('item1', 'item2')))
        self.assertTrue(Helper.is_sequence(array('l', [1, 2, 3, 4, 5])))
        self.assertTrue(Helper.is_sequence(array('d', [1.0, 2.0, 3.0, 4.0, 5.0])))
        self.assertTrue(Helper.is_sequence(bytearray.fromhex("deadbeef")))
        self.assertTrue(Helper.is_sequence(dict(one=1, two=2, three=3)))

        # testing non-sequential types
        self.assertFalse(Helper.is_sequence("Hello World"))
        self.assertFalse(Helper.is_sequence("Hello World\u203c"))
        self.assertFalse(Helper.is_sequence(3))
        self.assertFalse(Helper.is_sequence(3.14))
        self.assertFalse(Helper.is_sequence(self))
        self.assertFalse(Helper.is_sequence(None))
        self.assertFalse(Helper.is_sequence(True))
        self.assertFalse(Helper.is_sequence(Helper.is_sequence))

    def test_output(self):
        self.assertTrue(None == Helper.output("Test"))
        self.assertTrue(None == Helper.output("\u2031\u203c\u2049"))
        self.assertTrue(None == Helper.output(self))
        self.assertTrue(None == Helper.output(None))
        self.assertTrue(None == Helper.output(True))
        self.assertTrue(None == Helper.output(Helper.output))
        self.assertTrue(None == Helper.output(3))
        self.assertTrue(None == Helper.output(3.14))
        self.assertTrue(None == Helper.output(['a1', 'b2', 'c3']))
        self.assertTrue(None == Helper.output(('it1', 'it2')))
        self.assertTrue(None == Helper.output(array('l', [1, 2, 3, 4, 5])))
        self.assertTrue(None == Helper.output(array('B', [0x41, 0x42, 0x43, 0x44, 0x45])))
        self.assertTrue(None == Helper.output(bytearray.fromhex("deadbeef")))
        self.assertTrue(None == Helper.output(dict(one=1, two=2, three=3)))


def test_main():
    #test_support.run_unittest(HelperTestCase)
    #unittest.main()

    #suite = unittest.defaultTestLoader.loadTestsFromTestCase(HelperTestCase)
    #unittest.TextTestRunner().run(suite)

    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tcl = loader.loadTestsFromTestCase

    testClasses = [
        'HelperTestCase'
    ]

    for c in testClasses:
        suite.addTest(tcl(c))

    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    test_main()
