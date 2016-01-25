# Database Interface Module
import sqlite3

# Requires the file access module to pass the database location to it. Until then, the path will be passed manually
# TODO: Link file access to this
class Database():
	def __init__(self, dbname):
		self.conn = sqlite.connect(dbname)
		self.c = self.conn.cursor()
