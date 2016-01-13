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

class TestCreateTable(unittest.TestCase):
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

    def test_CreateDefaultTable_WrongType_Failure(self):
        """
        Try to test passing a table not supporting
        """
        table = None
        self.assertEqual(1, self.unit.create_table(table))

    def test_CreateDefaultTable_TableExists_Failure(self):
        """
        Try to test passing a table name, but it already exists
        """
        table = "MyTable"
        self.unit.create_table(table)
        self.assertEqual(1, self.unit.create_table(table))

    def test_CreateDefaultTable_TableNotExists_Success(self):
        """
        Try to test passing a table name, and it doesn't exist
        """
        table = "MyTable"
        self.assertEqual(0, self.unit.create_table(table))

class TestColumnName(unittest.TestCase):
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

    def test_DefaultTable_ColumnName(self):
        """
        Create a default table check the column name
        """
        table = "MyTable"
        self.unit.create_table(table)
        column = self.unit.read_column_info("MyTable")
        ipp = 0
        for col in column:
            if ipp == 0:
                self.assertEqual("id", col["name"].lower())
                self.assertEqual("integer", col["type"].lower())
            if ipp == 1:
                self.assertEqual("item", col["name"].lower())
                self.assertEqual("char(100)", col["type"].lower())
            if ipp == 2:
                self.assertEqual("value", col["name"].lower())
                self.assertEqual("blob", col["type"].lower())
            if ipp == 3:
                self.assertEqual("datetime", col["name"].lower())
                self.assertEqual("char(100)", col["type"].lower())
            ipp = ipp + 1

    def test_Table_ColumnName(self):
        """
        Create a default table check the column name
        """
        # Build a table to store into the database
        table = {}
        table["name"] = "Pagees"
        table["column"] = []
        table["column"].append({"name" : 'name', "type" : "String"})
        table["column"].append({"name" : 'comment', "type" : "str"})
        table["column"].append({"name" : 'status', "type" : "int"})
        self.unit.create_table(table)
        table_column_read = self.unit.read_column_info(table["name"])
        # Now rebuilt the table by adding the ID column naturaly
        # added by the API
        table = {}
        table["name"] = "Pagees"
        table["column"] = []
        table["column"].append({"name" : 'id', "type" : "integer"})
        table["column"].append({"name" : 'name', "type" : "char(100)"})
        table["column"].append({"name" : 'comment', "type" : "char(100)"})
        table["column"].append({"name" : 'status', "type" : "integer"})
        table["column"].append({"name" : 'datetime', "type" : "char(100)"})
        ipp = 0
        columns = zip(table["column"], table_column_read)
        for col in columns:
            if ipp == 0:
                self.assertEqual(col[0]["name"], col[1]["name"].lower())
                self.assertEqual(col[0]["type"], col[1]["type"].lower())
            if ipp == 1:
                self.assertEqual(col[0]["name"], col[1]["name"].lower())
                self.assertEqual(col[0]["type"], col[1]["type"].lower())
            if ipp == 2:
                self.assertEqual(col[0]["name"], col[1]["name"].lower())
                self.assertEqual(col[0]["type"], col[1]["type"].lower())
            if ipp == 3:
                self.assertEqual(col[0]["name"], col[1]["name"].lower())
                self.assertEqual(col[0]["type"], col[1]["type"].lower())
            if ipp == 4:
                self.assertEqual(col[0]["name"], col[1]["name"].lower())
                self.assertEqual(col[0]["type"], col[1]["type"].lower())
            ipp = ipp + 1




if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestCreateTable)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
    SUITE = unittest.TestLoader().loadTestsFromTestCase(TestColumnName)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
