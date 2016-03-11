#!/usr/bin/env python3

# Database Interface Module
import sqlite3

global dbrunning
dbrunning = []

# File access will initialise the class
class Database():
	def __init__(self, dbname):
		# Add to dbrunning list so it can always be refenced
		dbrunning.append(self)
		# Connect to database
		self.conn = sqlite3.connect(dbname)
		self.c = self.conn.cursor()
		
	def execute(self, statement, save=False):
		self.c.execute(statement)
		if save == True:
			self.commit()
		
	def commit(self):
		self.conn.commit()
		
	def close(self, save=True):
		if save == True:
			self.commit()
		self.conn.close()
		# Don't delete from dbrunning, or the values will shift - just set to None
		dbrunning[dbrunning.index(self)] = None
		del self
		
	def read(self, table, query=""):
		if query == "":
			self.c.execute('SELECT * FROM {0}'.format(table))
		else:
			self.c.execute('SELECT * FROM {0} WHERE {1}'.format(table, query))
		return self.c.fetchall()
		
	def write(self, table, values):
		dbid = self.nextAvail(table)
		if table == 'ticket_types':
			self.c.execute('INSERT INTO ticket_types (tName, tPrice, tInfo) VALUES {0}'.format(values))
		if table == 'user_info':
			self.c.execute('INSERT INTO user_info (fName, lName, code) VALUES {0}'.format(values))
		if table == 'orders':
			self.c.execute('INSERT INTO orders (quantity, userID, ticketTypeID) VALUES {0}'.format(values))
		return dbid
			
	def newEntry(self, fName, lName, randomID, tickets):
		for i in range(3):
			tickets[i] = str(tickets[i])
		# Find the database set ID while writing
		dbid = self.write("user_info", (fName, lName, randomID))
		# Enumerate returns a list with first item: index, second item: value
		for typ, quant in enumerate(tickets):
			# Only write orders to the database if there is 1 or more items
			if int(quant) > 0:
				self.write("orders", (quant, dbid, typ))
			
	def nextAvail(self, table):
		self.c.execute('SELECT max(ID) FROM {0}'.format(table))
		value = self.c.fetchone()[0]
		if value == None:
			return 1
		else:
			return value + 1
		
def newDB(path, keepalive=True):
	newdb = Database(path)
	newdb.execute('CREATE TABLE ticket_types (ID INTEGER PRIMARY KEY AUTOINCREMENT, tName TEXT, tPrice INTEGER, tInfo TEXT);')
	newdb.execute('CREATE TABLE user_info (ID INTEGER PRIMARY KEY AUTOINCREMENT, fName TEXT, lName TEXT, code CHAR(10));')
	newdb.execute('CREATE TABLE orders (ID INTEGER PRIMARY KEY AUTOINCREMENT, quantity INTEGER, userID INTEGER, ticketTypeID INTEGER);')
	newdb.commit()
	if not keepalive:
		newdb.close()
