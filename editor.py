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
		self.db = None
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
		
		self.window.show_all()
		
	def newdbfile(self):
		newdb = fileaccess.openDialog(self.window)
		if newdb != None:
			print("New File") # debug code
			try:
				self.db.close()
			except:
				pass
			self.db = newdb
			self.updateTickets()
			self.updateOrders()
			
	def updateTickets(self):
		for a,b in enumerate(self.db.read("ticket_types")):
			self.liststore1.append([str(b[1]), str(b[2]), str(b[3])])
			
	def updateOrders(self):
		for a, user in enumerate(self.db.read("user_info")):
			code = user[3]
			name = str(user[1] + " " + user[2])
			tickets = ""
			for b, order in enumerate(self.db.read("orders", "userID={0}".format(user[0]))):
				ticketname = self.db.read("ticket_types", "ID={0}".format(order[3]+1))[0][1]
				tickets += str(str(order[1]) + " " + ticketname + ", ")
			tickets = tickets[:-2]
			self.liststore2.append([code, name, tickets])
			
		
	# Close all windows on the deletion of the top-level window
	def on_window1_delete_event(self, *args):
		raise SystemExit(0)
		
	# New button
	def on_toolbutton1_clicked(self, *args):
		self.db = fileaccess.saveDialog(self.window, True)
	
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

	# Ticket Remove button
	def on_toolbutton6_clicked(self, *args):
		pass

	# Ticket Add button
	def on_toolbutton7_clicked(self, *args):
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
