#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import locale # Used for formatting strings to local currency
locale.setlocale( locale.LC_ALL, 'en_GB.UTF-8' )
import codegenerator
import dbinterface

# Start the reader program class
class Creator():
	def __init__(self):
		# Use the Gtk Builder to read the interface file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("creator.glade")
		self.builder.connect_signals(self)
		# Create the treeview list
		self.liststore1 = Gtk.ListStore(str, str)
		# Find items that need to be dynamic
		self.window = self.builder.get_object("window1")
		self.entry1 = self.builder.get_object("entry1")
		self.entry2 = self.builder.get_object("entry2")
		# Find the treeview object and attach a cell renderer to it
		self.treeview = self.builder.get_object("treeview1")
		# For every item in the list, create a column for it
		for i, column_title in enumerate(["Ticket Type", "Price"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)
		# Attach model to treeview
		self.treeview.set_model(self.liststore1)
		
		# Translate the database ticket types into a GUI list
		self.dbticket = dbinterface.dbrunning[database].read("ticket_types")
		self.tickets = []
		# For every ticket type, label a button for it
		for i in range(4):
			self.tickets.append([self.dbticket[i][1], str(locale.currency(self.dbticket[i][2]))])
			button = self.builder.get_object("button{0}".format(str(i+1)))
			button.set_label(self.dbticket[i][1])
			# Set a tooltip description that can be set by the user
			button.set_tooltip_text(self.dbticket[i][3])
		print(self.tickets) # debug code
		# Reset the table for first use
		self.clearTable()
		# With all elements set, show the window
		self.window.show_all()
	
	def onDeleteWindow(self, *args):
		# When the top-level window is closed, close everything
		Gtk.main_quit(*args)
	
	def addValue(self, value):
		# Add the ticket to the list view
		self.liststore1.append(self.tickets[value])
		# Also add to internal list
		self.ticketlist[value] += 1
		print(self.ticketlist) # debug code
		# Make sure the price is up to date
		self.updatePrice()
		
	def clearTable(self):
		# Make sure all lists are reset
		self.liststore1.clear()
		# Gtk lists are not very manageable - this is a more pythonic list that mirrors its changes
		self.ticketlist = [0,0,0,0]
		# Reset the name boxes
		self.entry1.set_text("")
		self.entry2.set_text("")
		# Create a new code for a new ticket
		self.code = codegenerator.codePrint(codegenerator.newCode(database))
		self.builder.get_object("label2").set_text(str("Code: "+self.code))
		# Set the price to 0 by updating it to the empty list
		self.updatePrice()
		
	def updatePrice(self):
		# Price starts as a 0 decimal number
		price = 0.0
		# Take each ticket in turn, and multiply it by the quantity
		for i in range(4):
			price += self.ticketlist[i] * self.dbticket[i][2]
		# Set the label object to show the price
		self.builder.get_object("label1").set_text(str(locale.currency(price)))
		
	# Link buttons and objects to events
	
	def on_button1_clicked(self, *args):
		self.addValue(0)
		
	def on_button2_clicked(self, *args):
		self.addValue(1)
		
	def on_button3_clicked(self, *args):
		self.addValue(2)

	def on_button4_clicked(self, *args):
		self.addValue(3)
	
	def on_clear_clicked(self, *args):
		self.clearTable()
	
	def on_open_clicked(self, *args):
		print("Open") # TODO: Link to file access
		
	def on_save_clicked(self, *args):
		# Fetch the names written into the text fields
		fName = self.entry1.get_text()
		lName = self.entry2.get_text()
		# Do not allow saving if fields are empty or read "Incomplete"
		if self.ticketlist != [0,0,0,0] and fName != "" and fName != "Incomplete" and lName != "" and lName != "Incomplete":
			# use the newEntry function to place all the info in the correct tables
			dbinterface.dbrunning[database].newEntry(fName, lName, self.code, self.ticketlist)
			# Once saved, clear the table for the next user
			self.clearTable()
			print(dbinterface.dbrunning[database].read("user_info")) # debug code
			print(dbinterface.dbrunning[database].read("orders")) # debug code
		# Alert the user to an incomplete section by setting "Incomplete" in it
		if fName == "":
			self.entry1.set_text("Incomplete")
		if lName == "":
			self.entry2.set_text("Incomplete")
		
# TODO: Create a file browser so it doesn't use the test database
dbinterface.sampleDB() # testing code
database = 0

# Assign the class and start the event loop
main = Creator() 
Gtk.main()
