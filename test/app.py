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
    PAGE["column"].append({"name" : 'name', "type" : "String"})
    PAGE["column"].append({"name" : 'comment', "type" : "str"})
    PAGE["column"].append({"name" : 'status', "type" : "int"})
    API.create_table(PAGE)
    ITEM = {}
    ITEM["name"] = "aParameter1"
    ITEM["comment"] = "ThisIsAnUpdate"
    ITEM["status"] = "OK"
    API.write(table=PAGE["name"], item=ITEM)
    ITEM = {}
    ITEM["name"] = "aParameter2"
    ITEM["comment"] = "ThisIsAnUpdate"
    ITEM["status"] = "OK"
    API.write(table=PAGE["name"], item=ITEM)
    API.write(table=PAGE["name"], item=ITEM)
    #print API.read(table="Pagees", item=ITEM)
    ITEM = {}
    ITEM["name"] = "aParameter1"
    print API.search_items(PAGE["name"], item=ITEM)
    ITEM["name"] = "aParameter2"
    print API.search_items(PAGE["name"], item=ITEM)
    API.exit()


