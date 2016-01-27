# Database Interface Module
import sqlite3

# Requires the file access module to pass the database location to it. Until then, the path will be passed manually
# TODO: Link file access to this
class Database():
	def __init__(self, dbname):
		self.conn = sqlite.connect(dbname)
		self.c = self.conn.cursor()
		
	def execute(self, statement):
		self.c.execute(statement)
		
	def commit(self):
		self.conn.commit()
		
	def close(self):
		self.conn.close()
		del self
		
	def write(self, table, values):
		if table == "userinfo":
			self.execute('INSERT INTO userinfo VALUES (?,?,?,?)', values)
		if table == "ticket_types":
			self.execute('INSERT INTO ticket_types VALUES (?,?,?,?)', values)
		if table == "orders":
			self.execute('INSERT INTO orders VALUES (?,?,?,?)', values)
		
		
def newDB(path):
	newdb = Database(path)
	newdb.execute('CREATE TABLE ticket_types (ID INT PRIMARY KEY NOT NULL, tName TEXT NOT NULL, tPrice INT NOT NULL, tInfo TEXT')
	newdb.execute('CREATE TABLE userinfo (ID INT PRIMARY KEY NOT NULL, fName TEXT NOT NULL, lName TEXT, randomID CHAR(10) NOT NULL')
	newdb.execute('CREATE TABLE orders (ID INT PRIMARY KEY NOT NULL, Quantity INT NOT NULL, userID INT NOT NULL, ticketTypeID INT NOT NULL')
	newdb.commit()
	newdb.close()
