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
from datetime import datetime

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
                print "WARNING: The database doesn't exist. I create an empty one from scratch"
            os.system("touch " + dbpath)
        else:
            if self.verbose:
                print "INFO: database found. Let's move foward!"
        self.sql.path = dbpath
        return 0

    def open(self):
        """
        Open sqlite3 database
        """
        self.sql.db3 = sqlite3.connect(self.sql.path)
        self.sql.cursor = self.sql.db3.cursor()

    def close(self):
        """
        Close sqlite3 database
        """
        self.sql.cursor.close()

    def exit(self):
        """
        Close sqlite3 database
        Initialize the db3 object
        """
        self.close()
        self.sql = None

    def create_table(self, table="defaultTable"):
        """
        Create a SQL table
        The function can be called with only a string arguments. if so,
        the function will create a table with the name you passed
        with two columns, parameter and value
        Else, the function you need to pass such structure:
            table is a dict
            table["name"]
            table["column"] = [{name, type}, {name, type}, ...]
        You can pass as much column you need. The type supported
        are int, float, string and raw
        The column is created only if another one doesn't exist
        """

        if type(table) is str:
            if self.search_table(table) is 0:
                if self.verbose:
                    print "INFO: Creating table \""+ table + "\""
                # Build the command
                cmd = "CREATE TABLE " + table + " (id INTEGER PRIMARY KEY, item CHAR(100) NOT NULL, value INTEGER NOT NULL)"
                # Store into the database
                self.sql.db3.execute(cmd)
                self.sql.db3.commit()

        elif type(table) is dict:
            if self.search_table(table["name"]) is 0:
                if self.verbose:
                    print "INFO: Creating table \""+ table["name"] + "\""
                # Build the command
                cmd = "CREATE TABLE "
                cmd += str(table["name"]) + " ( id INTEGER PRIMARY KEY,"
                for col in table["column"]:
                    cmd += " " + str(col["name"])
                    if "string" in col["type"].lower() or "str" in col["type"].lower():
                        cmd += " CHAR(100) NOT NULL,"
                    if "integer" in col["type"].lower() or "int" in col["type"].lower():
                        cmd += " INTEGER NOT NULL,"
                    if "float" in col["type"].lower() or "real" in col["type"].lower():
                        cmd += " REAL NOT NULL,"
                    if "blob" in col["type"].lower() or "raw" in col["type"].lower():
                        cmd += " BLOB,"
                cmd += " DATETIME CHAR(100) NOT NULL)"

                # Store into the database
                self.sql.db3.execute(cmd)
                self.sql.db3.commit()
        else:
            print "ERROR: No string or dict is passed"

    def read(self, table="defaultTable", item=None):
        """
        Read an entry in a table of the database
        """

    def write(self, table="defaultTable", item=None):
        """
        Write an entry in a table of the database
        """
        print "INFO: Write item in \"" + table + "\""
        cmd = "INSERT INTO " + table + " "
        (names, values) = self.format_items(item)
        cmd += names + values
        self.sql.db3.execute(cmd)
        self.sql.db3.commit()

    def update(self, table="defaultTable", item=None):
        """
        Update an entry in a table of the database
        """
        cmd = "UPDATE INTO " + table + " "
        (names, values) = self.format_items(item)
        cmd += names + values
        self.sql.db3.execute(cmd)
        self.sql.db3.commit()

    def search_table(self, table="defaultTable"):
        """
        Search an entry in a table of the database
        """
        ret = 0
        try:
            ret = self.sql.cursor.execute("SELECT 1 FROM " + str(table) + " LIMIT 1")
            ret = self.sql.cursor.fetchall()
        except:
            if self.verbose:
                print "INFO: searched table \""+ table + "\" is not defined"
        return ret

    def search_items(self, table="defaultTable", item=None):
        """
        Search an entry in a table of the database
        Require a dict with only one entry to filter the search
        """
        if item is not None:
            nname = ""
            for key in item.keys():
                nname = key
            cmd = "SELECT * FROM " + table + " WHERE " + nname + "=\"" + item[nname] + '\"'
            self.sql.cursor.execute(cmd)
            return self.sql.cursor.fetchall()
        else:
            if self.verbose:
                print "ERROR: item is not defined"
            return 1

    def delete(self, table="defaultTable", item=None):
        """
        Delete an entry in a table of the database
        """
        self.sql.db3.execute("DELETE FROM " + table  + "WHERE job=\"" + item["name"] + " \"")
        self.sql.db3.commit()

    def dump(self):
        """
        Dump the database to store it
        """

    def format_items(self, item=None):
        """
        from an item dict, return the strings name and values
        """
        ipp = 1
        names = "("
        values = "VALUES ("
        for elem in item.items():
            names += "\"" + str(elem[0]) + "\""
            if ipp != len(item):
                names += ", "
            else:
                names += ", DATETIME) "
            # And their values to update
            values += "\"" + str(elem[1]) + "\""
            if ipp != len(item):
                values += ", "
            else:
                values += ", \"" + str(datetime.now()) + "\") "
            ipp += 1
        return (names, values)

