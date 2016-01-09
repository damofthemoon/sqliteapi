"""
SQLite API and its sub-class
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bug in pylint leading to unfound some arguments of a function
# pylint: disable=E1120
# line too long
# pylint: disable=C0301
# too many lines in module
# pylint: disable=C0302

import os
import sqlite3

class DbObject(object):
    """
    An object containing the sqlite 3 database
    and its parameters/variables
    """
    def __init__(self, verbose=0):
        self.verbose = verbose
        self.path = None
        self.cursor = None
        self.db3 = None
        self.template = {}

    def get_template(self):
        """
        Get the template to see how to
        setup the template
        """
        return self.template

    def print_template(self):
        """
        Pretty print of the template
        to help user to build a table
        """
        print self.template

    def open(self):
        """
        Open sqlite3 database
        """
        self.db3 = sqlite3.connect(self.path)
        self.cursor = self.db3.cursor()

    def close(self):
        """
        Close sqlite3 database
        """
        self.cursor.close()


class SQLiteAPI(object):
    """
    SQLite API main class
    """

    def __init__(self, verbose=0, dbpath="./sqlite.db"):
        """
        Class constructor
        """
        self.open_flag = False
        self.verbose = 0
        self.set_verbose(verbose)
        self.sql = DbObject(self.verbose)
        self.set_dbpath(dbpath)

    def set_verbose(self, verbose=0):
        """
        Verbose mode setter
        """
        self.verbose = int(verbose)
        if self.verbose:
            print "INFO: verbose mode activated"
        return 0

    def set_dbpath(self, dbpath="./sqlite.db"):
        """
        Database path setter
        """
        if not os.path.isfile(dbpath):
            if self.verbose:
                print "ERROR: The database doesn't exist..."
            return 1
        self.sql.path = dbpath
        return 0

    def exit(self):
        """
        Close sqlite3 database
        Initialize the db3 object
        """
        self.sql.close()
        self.sql = None

    def create_page(self, page="default"):
        """
        Create a page, made in SQLite with a table
        """
        self.sql.db3.execute("CREATE TABLE " + page + " (id INTEGER PRIMARY KEY, job CHAR(100) NOT NULL, status INTEGER NOT NULL)")
        self.sql.db3.commit()

    def read(self, page="default", item=None):
        """
        Read an entry in a table of the database
        """

    def write(self, page="default", item=None):
        """
        Write an entry in a table of the database
        """

    def update(self, page="default", item=None):
        """
        Update an entry in a table of the database
        """
        self.sql.db3.execute("INSERT INTO " + page + " (job,status) VALUES ('" + item + "', -1)")
        self.sql.db3.commit()

    def search(self, page="default", item=None):
        """
        Search an entry in a table of the database
        """
        if item is not None:
            self.sql.cursor.execute("SELECT job,status FROM " + page + " WHERE job=\"" + item + '\"')
            return self.sql.cursor.fetchall()
        else:
            if self.verbose:
                print "ERROR: item is not defined"
            return 1

    def delete(self, page="default", item=None):
        """
        Delete an entry in a table of the database
        """
        self.sql.db3.execute("DELETE FROM " + page  + "WHERE job=\"" + item["name"] + " \"")
        self.sql.db3.commit()

    def dump(self):
        """
        Dump the database to store it
        """

