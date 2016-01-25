# Database Interface Module
import sqlite3

# Requires the file access module to pass the database location to it. Until then, the path will be passed manually
# TODO: Link file access to this
class Database():
	def __init__(self, dbname):
		self.conn = sqlite.connect(dbname)
		self.c = self.conn.cursor()
		
	def execute(statement):
		self.c.execute(statement)
		
	def commit():
		self.conn.commit()
		
	def close():
		self.conn.close()
		del self
		
def newDB():
	#TODO: Create a new database that fits the database schema exactly
