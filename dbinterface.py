#!/usr/bin/env python3

# Database Interface Module
import sqlite3

# Create a global variable to hold all the currently active databases

# File access will initialise the class
class Database():
	def __init__(self, path=":memory:"):
		if path == ":memory:":
			print("WARNING: Database is in memory! Nothing will be saved")
		# Connect to database
		self.conn = sqlite3.connect(path)
		self.c = self.conn.cursor()
		
	# By default, don't save to the database immediately
	def execute(self, statement, save=False):
		self.c.execute(statement)
		if save == True:
			self.commit()
	
	# Shortcut function for commit
	def commit(self):
		self.conn.commit()
	
	# Once the database is finished with, it can delete itself from memory
	def close(self, save=True):
		# If changes need to be discarded save can be set to False
		if save == True:
			self.commit()
		# Close the database connection
		self.conn.close()
		# Don't delete from dbrunning, or the values will shift - just set to None
		# dbrunning[dbrunning.index(self)] = None
		# Finally delete itself from memory to free up space
		del self
		
	# Basic table read function
	def read(self, table, query=""):
		if query == "":
			# By default the function returns all values
			self.c.execute('SELECT * FROM {0}'.format(table))
		else:
			# If a query is specified, run it
			self.c.execute('SELECT * FROM {0} WHERE {1}'.format(table, query))
		# After executing, remember to fetch the results
		return self.c.fetchall()
		
	# Basic table write funcation
	def write(self, table, values):
		# For program use, if they require the id that was set
		dbid = self.nextAvail(table)
		# Each table is different and also hardcoded, so different definitions are used for each
		if table == 'ticket_types':
			self.c.execute('INSERT INTO ticket_types (tName, tPrice, tInfo) VALUES {0}'.format(values))
		if table == 'user_info':
			self.c.execute('INSERT INTO user_info (fName, lName, code) VALUES {0}'.format(values))
		if table == 'orders':
			self.c.execute('INSERT INTO orders (quantity, userID, ticketTypeID) VALUES {0}'.format(values))
		# If a function needs the ID of the item created, it can catch this value
		return dbid
			
	# Uses the write function to sort data into the correct tables, with the correct foreign keys
	def newEntry(self, fName, lName, code, tickets):
		# The database takes all values of strings
		for i in range(3):
			tickets[i] = str(tickets[i])
		# Find the database set ID while writing to the database
		dbid = self.write("user_info", (fName, lName, code))
		# Enumerate returns a list with first item: index, second item: value
		for typ, quant in enumerate(tickets):
			# Only write orders to the database if there are 1 or more tickets
			if int(quant) > 0:
				self.write("orders", (quant, dbid, typ))
		self.commit()
		print("Entry Saved") # debug code
			
	# Find the next free ID
	def nextAvail(self, table):
		# Find the largest ID in the table
		self.c.execute('SELECT max(ID) FROM {0}'.format(table))
		value = self.c.fetchone()[0]
		if value == None:
			# If there are no IDs in the database, the next value must be 1
			return 1
		else:
			# If there are IDs, add 1 to the value found and return it
			return value + 1
			
	def verify(self):
		# Read the database schema from the sqlite_master table
		self.c.execute('SELECT * FROM sqlite_master')
		# Sample the data by taking the first value to see if it matches
		if self.c.fetchone() == ('table', 'ticket_types', 'ticket_types', 2, 'CREATE TABLE ticket_types (ID INTEGER PRIMARY KEY AUTOINCREMENT, tName TEXT, tPrice DECIMAL(10,2), tInfo TEXT)'):
			return True
		else:
			# If not, the table must be broken or incorrect
			return False
		
		
		
# Creates a new database with the correct tables
def newDB(path, keepalive=True):
	db = Database(path)
	db.execute('CREATE TABLE ticket_types (ID INTEGER PRIMARY KEY AUTOINCREMENT, tName TEXT, tPrice DECIMAL(10,2), tInfo TEXT);')
	db.execute('CREATE TABLE user_info (ID INTEGER PRIMARY KEY AUTOINCREMENT, fName TEXT, lName TEXT, code CHAR(10));')
	db.execute('CREATE TABLE orders (ID INTEGER PRIMARY KEY AUTOINCREMENT, quantity INTEGER, userID INTEGER, ticketTypeID INTEGER);')
	db.commit()
	# If the database is not needed right now, close it after creation
	if not keepalive:
		db.close()
	else:
		# Give the database object
		return db

# Purely for debugging and testing purposes. Create an already populated database for test usage
def sampleDB(path=":memory:"):
	db = newDB(path)
	db.write("ticket_types", ("Adult", "20.08", "A fully grown human being."))
	db.write("ticket_types", ("Child", "10.50", "A slightly smaller human being."))
	db.write("ticket_types", ("Student", "12.10", "A youthful human being."))
	db.write("ticket_types", ("Senior", "18.46", "An old human being."))
	db.write("user_info", ("Elvin", "Luff", "001E5CBC5"))
	db.write("orders", ("3", "1", "1"))
	db.write("orders", ("5", "1", "3"))
	return db
