#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader
import dbinterface
import fileaccess

# Start the reader program class
class Editor():
	def __init__(self):
		# Use the Gtk Builder to read the interface file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("editor.glade")
		self.builder.connect_signals(self)
		# Create the treeview list
		#self.liststore1 = Gtk.ListStore(str, str)
		# Find items that need to be dynamic
		self.window = self.builder.get_object("window1")
		#self.entry1 = self.builder.get_object("entry1")
		#self.entry2 = self.builder.get_object("entry2")
		# Find the treeview object and attach a cell renderer to it
		#self.treeview = self.builder.get_object("treeview1")
		# For every item in the list, create a column for it
		#for i, column_title in enumerate(["Ticket Type", "Price"]):
		#	renderer = Gtk.CellRendererText()
		#	column = Gtk.TreeViewColumn(column_title, renderer, text=i)
		#	self.treeview.append_column(column)
		# Attach model to treeview
		#self.treeview.set_model(self.liststore1)
		
		# Translate the database ticket types into a GUI list
		#self.dbticket = dbinterface.dbrunning[database].read("ticket_types")
		#self.tickets = []
		#print(self.tickets) # debug code
		# Reset the table for first use
		#self.clearTable()
		# With all elements set, show the window
		self.window.show_all()
		
	# Close all windows on the deletion of the top-level window
	def on_window1_delete_event(self, *args):
		Gtk.main_quit(*args)
		
	def on_toolbutton1_clicked(self, item):
		try:
			fileaccess.setFile(fileaccess.openDialog(self.window))
		except (NameError, TypeError):
			print("nope")

# For testing - Use the sample database	
dbinterface.sampleDB()
database = 0

# Create the main event loop
main = Editor()
Gtk.main()
