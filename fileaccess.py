#!/usr/bin/env python3

# File Access Module

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dbinterface import *
#from shutil import copyfile

def setFile(path):
	# Validate that it is a database file if the last 3 characters are .db
	if path[-3:] != '.db':
		raise TypeError
	# Try opening the database. Remember to catch exceptions
	db = Database(path)
	# Verify that the database is for this program
	if db.verify() == False:
		# If not, remember to close the database without saving anything to it
		db.close(False)
		raise TypeError
	# Return the new database object
	return db
	
def newFile(path):
	# Make sure the new file has the correct ending
	if path[-3:] != ".db":
		path += ".db"
	return path

# Create a dialog box for selecting the sqlite file
def openDialog(parent=None):
	# Create the dialog object
	dialog = Gtk.FileChooserDialog("Please choose a file", parent, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
	# Run the dialog object, catching responses
	response = dialog.run()
	# Process the response
	if response == Gtk.ResponseType.OK:
		print("File selected: " + dialog.get_filename()) # debug code
		# If the file is not correct, an error will occur, so catch it
		try:
			# Pass to setFile to validate and open the database
			response = setFile(dialog.get_filename())
		# If it is an error, send None
		except (TypeError, NameError):
			response = None
			print("This is an invalid file!") # debug code
	# If cancel is pressed, send None
	elif response == Gtk.ResponseType.CANCEL:
		print("Cancel clicked") # debug code
		response = None
	# Remember to get rid of the dialog box
	dialog.destroy()
	# Return the database object
	return response

def saveDialog(parent=None, db=None):
	# Create the dialog object
	dialog = Gtk.FileChooserDialog("Save Database As...", parent, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
	# Run the dialog object, catching responses
	response = dialog.run()
	# Process the response
	if response == Gtk.ResponseType.OK:
		print("File selected: " + dialog.get_filename()) # debug code
		# If the file is not correct, an error will occur, so catch it
		try:
			if db == None:
				response = newDB(newFile(dialog.get_filename()))
			else:
				db.commit()
				# TODO: work out how I'm going to get save as working
		# If it is an error, send None
		except (TypeError, NameError):
			response = None
			print("This is an invalid file!") # debug code
	# If cancel is pressed, send None
	elif response == Gtk.ResponseType.CANCEL:
		print("Cancel clicked") # debug code
		response = None
	# Remember to get rid of the dialog box
	dialog.destroy()
	# Return the database object
	return response
