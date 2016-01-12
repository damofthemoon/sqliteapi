#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Unit tests
"""
# bug in pylint leading to unfound some arguments of a function
# pylint: disable=E1120
# line too long
# pylint: disable=C0301
# too many lines in module
# pylint: disable=C0302

import os
import sys
import unittest
sys.path.append("./src")
from sqlite_api import SQLiteAPI

class TestSQLiteAPI(unittest.TestCase):
    """
    Testsuite 1 to test map function
    """
    def setUp(self):
        """
        Setup function launched before a testcase
        """
        self.dbpath = 'test/db.db3'
        self.unit = SQLiteAPI(verbose=1, dbpath=self.dbpath)
        self.unit.open()

    def tearDown(self):
        """
        tearDown function launched after a testcase
        """
        os.system("rm -fr " + self.dbpath)

    #def test_createDefault_table_Failure(self):
    #    """
    #    First test stressing the square function
    #    """
    #    TABLE = None
    #    self.assertEqual(1, self.unit.create_table(TABLE))
    #   os.system("rm -fr " + self.dbpath)

    def test_createDefaultTable_TableExists_Failure(self):
        """
        First test stressing the square function
        """
        TABLE = "MyTable"
        self.unit.create_table()
        self.assertEqual(1, self.unit.create_table(TABLE))
        os.system("rm -fr " + self.dbpath)

    #def test_createDefaultTable_TableNotExists_Success(self):
    #    """
    #    First test stressing the square function
    #    """
    #    TABLE = "MyTable"
    #    self.assertEqual(0, self.unit.create_table(TABLE))
    #    os.system("rm -fr " + self.dbpath)


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestSQLiteAPI)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
