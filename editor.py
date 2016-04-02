#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import locale # Used for formatting strings to local currency
locale.setlocale( locale.LC_ALL, 'en_GB.UTF-8' )
import codereader
import dbinterface
import fileaccess

# Start the reader program class
class Editor():
	def __init__(self):
		self.firstrun = True
		# Use the Gtk Builder to read the interface file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("editor.glade")
		self.builder.connect_signals(self)
		# Create the treeview list
		self.liststore1 = Gtk.ListStore(str, str, str)
		# Find items that need to be dynamic
		self.window = self.builder.get_object("window1")
		# Find the treeview object and attach a cell renderer to it
		self.treeview1 = self.builder.get_object("treeview1")
		# For every item in the list, create a column for it
		for i, column_title in enumerate(["Ticket Type", "Price", "Information"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview1.append_column(column)
		# Attach model to treeview
		self.treeview1.set_model(self.liststore1)
		
		self.liststore2 = Gtk.ListStore(str, str, str)
		# Find the treeview object and attach a cell renderer to it
		self.treeview2 = self.builder.get_object("treeview2")
		# For every item in the list, create a column for it
		for i, column_title in enumerate(["Ticket Code", "Name", "Orders"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview2.append_column(column)
		# Attach model to treeview
		self.treeview2.set_model(self.liststore2)
		self.status = self.builder.get_object("statusbar1")
		self.status.push(self.status.get_context_id(""), "Welcome to the Ticket Editor! Open or create a database to continue.")

		self.window.show_all()
		
	def newdbfile(self):
		# Use the Open dialog to get a database path
		newdb = fileaccess.openDialog(self.window)
		# Do nothing if no path is given/valid
		if newdb != None:
			# Close the old database, if it exists
			try:
				self.db.close()
			except:
				pass
			# Reassign the current database
			self.db = newdb
			# Update both tables with the new database information
			self.updateTickets()
			self.updateOrders()
			if self.firstrun == True:
				# Active all buttons once a database is opened
				self.builder.get_object("toolbutton4").set_sensitive(True)
				self.builder.get_object("toolbutton5").set_sensitive(True)
				self.builder.get_object("toolbutton6").set_sensitive(True)
				self.builder.get_object("toolbutton8").set_sensitive(True)
				self.builder.get_object("toolbutton9").set_sensitive(True)
				self.firstrun = False
			self.status.push(self.status.get_context_id(""), "Database opened successfully!")
		else:
			self.status.push(self.status.get_context_id(""), "The file you've selected is invalid. Please try another.")
			
	# Take the information from ticket_types and display everything
	def updateTickets(self):
		self.liststore1.clear()
		# For each line in the table, display all columns except the ID column
		for a,b in enumerate(self.db.read("ticket_types")):
			self.liststore1.append([str(b[1]), str(locale.currency(b[2])), str(b[3])])
			
	# We need to present each order in a way that the user can read, bringing the data in from all tables.
	def updateOrders(self):
		self.liststore2.clear()
		# We need a row for every user
		for a, user in enumerate(self.db.read("user_info")):
			# Take the ticket code and use for the first row
			code = user[3]
			# Combine the first and last names into the second row
			name = str(user[1] + " " + user[2])
			# Finding the ticket quantity and then name requires multiple queries
			tickets = ""
			# Repeat for each order attached to the user
			for b, order in enumerate(self.db.read("orders", "userID={0}".format(user[0]))):
				# Query the ticket_types table for the correct ticket name
				ticketname = self.db.read("ticket_types", "ID={0}".format(order[3]+1))[0][1]
				# Take the order quantity and the ticket name and place in a string
				tickets += str(str(order[1]) + " " + ticketname + ", ")
			# Remove the last ", "
			tickets = tickets[:-2]
			# Finally, take the row and append it to the table
			self.liststore2.append([code, name, tickets])
			
		
	# Close all windows on the deletion of the top-level window
	def on_window1_delete_event(self, *args):
		raise SystemExit(0)
		
	# New button
	def on_toolbutton1_clicked(self, *args):
		self.db = fileaccess.saveDialog(self.window)
		self.updateOrders()
		self.updateTickets()
	
	# Open button
	def on_toolbutton2_clicked(self, *args):
		self.newdbfile()

	# Save button
	def on_toolbutton4_clicked(self, *args):
		self.db.commit()

	# Save As button
	def on_toolbutton5_clicked(self, *args):
		self.db.commit()
		self.db = fileaccess.saveDialog(self.window)

	# Ticket Edit button
	def on_toolbutton6_clicked(self, *args):
		pass

	# Order Remove button	
	def on_toolbutton8_clicked(self, *args):
		pass

	# Order Add button
	def on_toolbutton9_clicked(self, *args):
		pass

# Create the main event loop
main = Editor()
Gtk.main()
