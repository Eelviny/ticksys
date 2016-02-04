# Database Interface Module
import sqlite3

# Requires the file access module to pass the database location to it. Until then, the path will be passed manually
# TODO: Link file access to this
class Database():
	def __init__(self, dbname):
		self.conn = sqlite3.connect(dbname)
		self.c = self.conn.cursor()
		
	def execute(self, statement):
		self.c.execute(statement)
		
	def commit(self):
		self.conn.commit()
		
	def close(self):
		self.conn.close()
		del self
		
	def read(self, table, query=""):
		if query == "":
			self.execute('SELECT * FROM ?', table)
		else:
			query = [table, query]
			self.execute('SELECT * FROM ? WHERE ?', query)
		return self.c.fetchall()
		
	def write(self, table, values):
		if table == 'ticket_types':
			self.execute('INSERT INTO ticket_types (tName, tPrice, tInfo) VALUES (?,?,?)', values)
		if table == 'userinfo':
			self.execute('INSERT INTO userinfo (fName, lName, randomID) VALUES (?,?,?)', values)
		if table == 'orders':
			self.execute('INSERT INTO orders (quantity, userID, ticketTypeID) VALUES (?,?,?)', values)
			
	def nextAvail(self):
		self.c.lastrowid
		
		
def newDB(path):
	newdb = Database(path)
	newdb.execute('CREATE TABLE ticket_types (ID INTEGER PRIMARY KEY AUTOINCREMENT, tName TEXT, tPrice INTEGER, tInfo TEXT);')
	newdb.execute('CREATE TABLE userinfo (ID INT PRIMARY KEY AUTOINCREMENT, fName TEXT, lName TEXT, randomID CHAR(10));')
	newdb.execute('CREATE TABLE orders (ID INT PRIMARY KEY AUTOINCREMENT, quantity INTEGER, userID INTEGER, ticketTypeID INTEGER);')
	newdb.commit()
	newdb.close()
