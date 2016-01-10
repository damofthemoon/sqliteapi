#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bug in pylint leading to unfound some arguments of a function
# pylint: disable=E1120
# line too long
# pylint: disable=C0301
# too many lines in module
# pylint: disable=C0302

import os
import sys
sys.path.append("src")

from sqlite_api import SQLiteAPI

if __name__ == '__main__':
    
    os.system("rm -fr test/db.db3")
    API = SQLiteAPI(verbose=1, dbpath="test/db.db3")
    API.open()
    API.create_table()
    PAGE = {}
    PAGE["name"] = "Pagees"
    PAGE["column"] = []
    PAGE["column"].append({"name" : 'aParameter', "type" : "String"})
    PAGE["column"].append({"name" : 'aComment', "type" : "str"})
    PAGE["column"].append({"name" : 'aStatus', "type" : "int"})
    API.create_table(PAGE)
    API.exit()


