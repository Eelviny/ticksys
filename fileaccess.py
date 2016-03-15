#!/usr/bin/env python3

# File Access Module

from dbinterface import *

def setFile(path):
	# Validate that it is a database file if the last 3 characters are .db
	if path[-3:] != '.db':
		raise NameError
	# Try opening the database. Remember to catch exceptions
	opendb = Database(path)
	# Verify that the database is for this program
	if opendb.verify() == False:
		raise NameError
	# Only create a new entry if it's not there - no duplicates
	if opendb not in dbrunning:
		dbrunning.append(opendb)
	# Return the value of position in the list
	return dbrunning.index(opendb)
	
def newFile(path):
	# Make sure the new file has the correct ending
	if path[-3:] != ".db":
		path += ".db"
	return newDB(filestring)
