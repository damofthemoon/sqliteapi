# SQLiteAPI

## PURPOSE
* SQLiteAPI provides an easy way to use and manage an SQLite 3 database.
* Simple and limited but done to replace a XML, JSON or text file to store data
* Python 2.7

## API DESCRIPTION
### INIT
* Used to initialize the class
* self.open-flag
* self.dbpath
* self.verbose
* self.cursor = None
* self.setup()

### SETUP.VERBOSE
* Set self.verbose

### SETUP.DB
* If self.open-flag, self.close()
* If dbpath, set self.dbpath

### OPEN
* If dbpath, self.setupdb()
* If not self.open-flag, self.open()

### CLOSE
* If self.open-flag, self.close() database

### EXIT
* Close database with self.close()
* Initialize internal variables

### READ
* If not self.open-flag, self.open()
* Read database entry into a database\'s table
* If exists, return entry, else 1

### WRITE
* If not self.open-flag, self.open()
* Self.search(), if exists, return 1, else:
* Write database entry into a database's table
* Return 0

### UPDATE
* If not self.open-flag, self.open()
* Update database entry
    * Read database to self.search() element into a database's table
    * If doesn't exist self.write()
    * Else write a new value into

### DELETE
* If not self.open-flag, self.open()
* Delete database entry
    *   Read database to self.search() element into a database's table or into the whole database
    * If exists, delete it, else return 1

### SEARCH
* If not self.open-flag, self.open()
* Search an entry into a database's table
* Return entry if exists, else 1

### DUMP
* Do a dummy dump of the database's past instructions for backup purpose.

