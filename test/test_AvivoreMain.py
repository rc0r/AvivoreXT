# -*- coding: utf-8 -*-

import unittest
from AvivoreXT import AvivoreMain, AvivoreError
import os
import shutil


class AvivoreMainTestCase(unittest.TestCase):
    def setUp(self):
        # code to execute in preparation for tests
        os.symlink('../sample.conf', './testdata/test.conf')
        os.symlink('../sample_conf.db', './testdata/test.db')

    def tearDown(self):
        # code to execute to clean up after tests
        os.remove('./testdata/test.conf')
        os.remove('./testdata/test.db')

    def test_check_usage(self):
        args = [
            'prog_name',
            '-c',
            'config_file',
        ]
        self.assertIsNone(AvivoreMain.check_usage(args))

        args = [
            'prog_name',
            '-d',
            'config_database',
        ]
        self.assertIsNone(AvivoreMain.check_usage(args))

        args = [
            'prog_name',
            '-e',
            'config_file',
        ]
        with self.assertRaises(AvivoreError.AvivoreError):
            self.assertIsNone(AvivoreMain.check_usage(args))

        args = [
            'prog_name',
            '-c',
        ]
        with self.assertRaises(AvivoreError.AvivoreError):
            self.assertIsNone(AvivoreMain.check_usage(args))

        args = [
            'prog_name',
            '-c',
            'config_file',
            'too_much',
        ]
        with self.assertRaises(AvivoreError.AvivoreError):
            self.assertIsNone(AvivoreMain.check_usage(args))

    def test_software_init_msg(self):
        self.assertIsNone(AvivoreMain.software_init_msg('1.2.3'))

    def test_main(self):
        args = [
            'prog_name',
            '-c',
            './testdata/test.conf'
        ]
        self.assertIsNone(AvivoreMain.main(args, True))

        args = [
            'prog_name',
            '-d',
            './testdata/test.db'
        ]
        self.assertIsNone(AvivoreMain.main(args, True))

        args = [
            'prog_name',
            '-e',
            './testdata/test.conf'
        ]
        self.assertIs(AvivoreMain.main(args, True), -1)

    def test_start(self):
        pass


def test_main():
    unittest.main()


if __name__ == '__main__':
    test_main()
