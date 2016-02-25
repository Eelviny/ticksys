# Database Interface Module
import sqlite3

global opendbs
opendbs = []

# File access will initialise the class
class Database():
	def __init__(self, dbname):
		self.conn = sqlite3.connect(dbname)
		self.c = self.conn.cursor()
		
	#def execute(self, statement):
	#	self.c.execute(statement)
		
	def commit(self):
		self.conn.commit()
		
	def close(self):
		self.conn.close()
		del self
		
	def read(self, table, query=""):
		if query == "":
			self.c.execute('SELECT * FROM {0}'.format(table))
		else:
			self.c.execute('SELECT * FROM {0} WHERE {1}'.format(table, query))
		return self.c.fetchall()
		
	def write(self, table, values):
		if table == 'ticket_types':
			self.c.execute('INSERT INTO ticket_types (tName, tPrice, tInfo) VALUES (?,?,?)', values)
		if table == 'userinfo':
			self.c.execute('INSERT INTO userinfo (fName, lName, randomID) VALUES (?,?,?)', values)
		if table == 'orders':
			self.c.execute('INSERT INTO orders (quantity, userID, ticketTypeID) VALUES (?,?,?)', values)
			
	def nextAvail(self):
		self.c.lastrowid
		
		
def newDB(path, keepalive=True):
	newdb = Database(path)
	opendbs.append(newdb)
	newdb.c.execute('CREATE TABLE ticket_types (ID INTEGER PRIMARY KEY AUTOINCREMENT, tName TEXT, tPrice INTEGER, tInfo TEXT);')
	newdb.c.execute('CREATE TABLE userinfo (ID INTEGER PRIMARY KEY AUTOINCREMENT, fName TEXT, lName TEXT, randomID CHAR(10));')
	newdb.c.execute('CREATE TABLE orders (ID INTEGER PRIMARY KEY AUTOINCREMENT, quantity INTEGER, userID INTEGER, ticketTypeID INTEGER);')
	newdb.commit()
	if not keepalive:
		newdb.close()
