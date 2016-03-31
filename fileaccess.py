#!/usr/bin/env python3

# File Access Module

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from dbinterface import *

def setFile(path):
	# Validate that it is a database file if the last 3 characters are .db
	if path[-3:] != '.db':
		raise TypeError
	# Try opening the database. Remember to catch exceptions
	opendb = Database(path)
	# Verify that the database is for this program
	if opendb.verify() == False:
		raise TypeError
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
	
def openDialog(parent=None):
	dialog = Gtk.FileChooserDialog("Please choose a file", parent, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		print("Open clicked")
		print("File selected: " + dialog.get_filename())
	elif response == Gtk.ResponseType.CANCEL:
		print("Cancel clicked")
	dialog.destroy()

def saveDialog(parent=None):
	dialog = Gtk.FileChooserDialog("Please choose a location", parent, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
	response = dialog.run()
	if response == Gtk.ResponseType.OK:
		print("File selected: " + dialog.get_filename())
		response = dialog.get_filename()
	elif response == Gtk.ResponseType.CANCEL:
		print("Cancel clicked")
		response = None
	dialog.destroy()
	return response
