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
                cmd = "CREATE TABLE " + table + " (id INTEGER PRIMARY KEY, item CHAR(100) NOT NULL, value BLOB, DATETIME CHAR(100) NOT NULL)"
                # Store into the database
                self.sql.db3.execute(cmd)
                self.sql.db3.commit()
                return 0
            else:
                return 1

        elif type(table) is dict:
            if self.search_table(table["name"]) is 0:
                if self.verbose:
                    print "INFO: Creating table \""+ table["name"] + "\""
                # Build the command
                cmd = "CREATE TABLE "
                cmd += str(table["name"]) + " ( id INTEGER PRIMARY KEY,"
                for col in table["column"]:
                    cmd += " " + str(col["name"])
                    if "string" in col["type"].lower() or "str" in col["type"].lower() or "char" in col["type"].lower():
                        cmd += " CHAR(100),"
                        #cmd += " CHAR(100) NOT NULL,"
                    if "integer" in col["type"].lower() or "int" in col["type"].lower():
                        cmd += " INTEGER,"
                        #cmd += " INTEGER NOT NULL,"
                    if "float" in col["type"].lower() or "real" in col["type"].lower():
                        cmd += " REAL,"
                        #cmd += " REAL NOT NULL,"
                    if "blob" in col["type"].lower() or "raw" in col["type"].lower():
                        cmd += " BLOB,"
                cmd += " DATETIME CHAR(100))"
                #cmd += " DATETIME CHAR(100) NOT NULL)"

                # Store into the database
                self.sql.db3.execute(cmd)
                self.sql.db3.commit()
                return 0
            else:
                return 1
        else:
            print "ERROR: No string or dict is passed"
            return 1

    def read(self, table="defaultTable", filters=None):
        """
        Read an entry in a table of the database
        Read a dict as input containing column to filter
        Always return all the columns
        """
        ipp = 1
        if type(table) is not str:
            print "ERROR: table name must be s tring"
            return 1

        if filters is None and type(filters) is not dict:
            print "ERROR: filters to search for the entries must be ordered in a dict"
            return 1

        if self.verbose:
            print "INFO: Read entries in " + table

        cmd = "SELECT * FROM " + table + " WHERE ( "
        # Extract the filters to use for search
        for key in filters.keys():
            cmd += key + "=\"" + filters[key] + '\"'
            if ipp != len(filters):
                cmd += " AND "
                ipp += 1
            else:
                cmd += " );"

        # Read the values into the table
        self.sql.cursor.execute(cmd)
        _vals = self.sql.cursor.fetchall()
        # Read the column names
        _cols = self.read_column_info(table)
        ret_items = []
        # Now parse each lines read into the database
        for __vals in _vals:
            ret_item = []
            # Now combine each column name and its values into
            # a list of dict( "name", "value")
            for (_col, _val) in zip(_cols, list(__vals)):
                dit = dict()
                dit["name"] = _col["name"]
                dit["value"] = _val
                ret_item.append(dit)
            if len(_vals) == 1:
                return ret_item
            else:
                ret_items.append(ret_item)
        return ret_items


    def write(self, table="defaultTable", item=None):
        """
        Write an entry in a table of the database
        """
        if type(item) is dict:
            print "INFO: Write item in \"" + table + "\""
            cmd = "INSERT INTO " + table + " "
            (names, values) = self.format_items_for_write(item)
            cmd += names + values
            self.sql.db3.execute(cmd)
            self.sql.db3.commit()
            return 0
        else:
            print "ERROR: item passed for write command is not a dict"
            return 1


    def update(self, table="defaultTable", item=None, new_item=None):
        """
        Update an entry in a table of the database
        """
        ipp = 1
        cmd = "UPDATE " + table + " SET "
        # First order the values to update
        if new_item is not None and type(new_item) is dict:
            # Extract the key's name to search for
            for key in new_item.keys():
                cmd += key + "=\"" + new_item[key] + "\""
                if ipp != len(new_item):
                    cmd += ", "
                    ipp += 1
        # Then order the value used to identify the line(s)
        ipp = 1
        cmd += " WHERE "
        if item is not None and type(item) is dict:
            # Extract the key's name to search for
            for key in item.keys():
                cmd += key + "=\"" + item[key] + "\""
                if ipp != len(item):
                    cmd += ", "
                    ipp += 1
                else:
                    cmd += ";"
        # Execute the command line and return the status
        self.sql.cursor.execute(cmd)
        return 0

    def delete(self, table="defaultTable", filters=None):
        """
        Delete an entry in a table of the database
        """
        if type(table) is not str:
            print "ERROR: table name must be s tring"
            return 1

        if filters is None and type(filters) is not dict:
            print "ERROR: filters to search for the entries must be ordered in a dict"
            return 1

        # Extract the key's name to search for
        cmd = "DELETE FROM " + table + " WHERE ( "
        ipp = 1
        # Extract the filters to use for search
        for key in filters.keys():
            cmd += key + "=\"" + filters[key] + '\"'
            if ipp != len(filters):
                cmd += " AND "
                ipp += 1
            else:
                cmd += " );"

        try:
            self.sql.db3.execute(cmd)
            self.sql.db3.commit()
            return 0
        except:
            print "ERROR: delete command has not been executed"
            return 1

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

    def read_column_info(self, table="defaultTable"):
        """
        Return the column names of the table
        """
        cmd = "PRAGMA table_info('" + table + "')"
        self.sql.cursor.execute(cmd)
        infos = self.sql.cursor.fetchall()
        column_info = []
        for info in infos:
            col = {}
            col["id"] = str(info[0]).encode("utf-8")
            col["name"] = str(info[1]).encode("utf-8")
            col["type"] = str(info[2]).encode("utf-8")
            column_info.append(col)
        return column_info

    def format_items_for_write(self, item=None):
        """
        from an item dict, return the strings name and values
        """
        ipp = 1
        names = "("
        values = "VALUES ("
        for elem in item.items():
            names += "\"" + str(elem[0]) + "\""
            values += "\"" + str(elem[1]) + "\""
            if ipp != len(item):
                names += ", "
                values += ", "
            else:
                names += ", DATETIME) "
                values += ", \"" + str(datetime.now()) + "\") "
            ipp += 1
        return (names, values)

    def dump(self):
        """
        Dump the database to store it
        """
        # TODO: Return the dump output, not just the return code
        os.system("sqlite3 .dump " + self.sql.path)


