# SQLiteAPI

## PURPOSE
* SQLiteAPI provides an easy way to use and manage an SQLite 3 database.
* Simple and limited but done to replace a XML, JSON or text file to store data
* Python 2.7

## API DESCRIPTION

### __INIT__
* Used to initialize the class
* self.sql: object containing the sqlite3 object
* self.open_flag: internal flag to open or close the database
* self.dbpath: string to store path to db3 file
* self.verbose: verbose mode 0 or 1

### SET_VERBOSE()
* Set self.verbose

### SET_DB_PATH()
* Set self.sql.dbpath

### OPEN()
* If not self.open-flag, self.open()

### CLOSE()
* If self.open-flag, self.close() database

### EXIT()
* Close database with self.close()
* Initialize internal variables

### READ()
* self.open()
* Read database entry into a database\'s table by using filter
* Sort columns returns by adding the column name for each entry(ies)
* If exists, return entry, else 1

### WRITE()
* self.open()
* Write database entry into a database's table
* Return 0

### UPDATE()
* self.open()
* If not self.open-flag, self.open()
* Update database entry
    * search for all entries complying filters
    * updates the fields specified

### DELETE()
* self.open()
* Delete database entry
    * Read database to self.search() element into a database's table or into the whole database
    * If exists, delete it, else return 1

### SEARCH()
* self.open()
* Search an entry into a database's table
* Return entry if exists, else 1

### DUMP()
* Do a dummy dump of the database's past instructions for backup purpose.

