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
		self.liststore1 = Gtk.ListStore(int, str, str, str)
		# Find items that need to be dynamic
		self.window = self.builder.get_object("window1")
		# Find the treeview object and attach a cell renderer to it
		treeview1 = self.builder.get_object("treeview1")
		# For every item in the list, create a column for it
		for i, column_title in enumerate(["#", "Ticket Type", "Price", "Information"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			treeview1.append_column(column)
		# Attach model to treeview
		treeview1.set_model(self.liststore1)
		
		self.liststore2 = Gtk.ListStore(str, str, str)
		# Find the treeview object and attach a cell renderer to it
		treeview2 = self.builder.get_object("treeview2")
		# For every item in the list, create a column for it
		for i, column_title in enumerate(["Ticket Code", "Name", "Orders"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			treeview2.append_column(column)
		# Attach model to treeview
		treeview2.set_model(self.liststore2)
		self.statusPush("Welcome to the Ticket Editor! Open or create a database to continue.")

		self.window.show_all()
	
	def statusPush(self, message):
		status = self.builder.get_object("statusbar1")
		status.push(status.get_context_id(""), message)
		
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
			self.statusPush("Database opened successfully!")
		else:
			self.statusPush("The file you've selected is invalid. Please try another.")
			
	# Take the information from ticket_types and display everything
	def updateTickets(self):
		self.liststore1.clear()
		# For each line in the table, display all columns except the ID column
		for a,b in enumerate(self.db.read("ticket_types")):
			self.liststore1.append([int(b[0]), str(b[1]), str(locale.currency(b[2])), str(b[3])])
			
	# We need to present each order in a way that the user can read, bringing the data in from all tables.
	def updateOrders(self):
		self.liststore2.clear()
		for i in self.db.returnOrders():
			name = i[0] + " " + i[1]
			code = i[2]
			tickets = ""
			for a, b in enumerate(i[3]):
				if b != 0:
					typename = self.db.read("ticket_types", "ID={0}".format(a+1))[0][1]
					tickets += str(str(b) + " " + typename + ", ")
			tickets = tickets[:-2]
			self.liststore2.append([code, name, tickets])

	def orderPopup(self, code=None):
		self.omode = code
		popup = self.builder.get_object("window2")
		for i in range(1,5):
			self.builder.get_object("label{0}".format(i)).set_text(self.db.read("ticket_types", "ID={0}".format(i))[0][1] + " Ticket")
		if code == None:
			user = ["", "", "", [0, 0, 0, 0]]
		else:
			user = self.db.returnOrders("code='{0}'".format(code))[0]
		self.builder.get_object("entry1").set_text(user[0])
		self.builder.get_object("entry2").set_text(user[1])
		for i in range(4):
			self.builder.get_object("adjustment{0}".format(i+1)).set_value(user[3][i])
		popup.show_all()
		
	def ticketPopup(self, dbid=None):
		self.tmode = dbid
		popup = self.builder.get_object("window3")
		if dbid == None:
			ticket = (1, '', 0.00, '')
		else:
			ticket = self.db.read("ticket_types", "ID='{0}'".format(dbid))[0]
		self.builder.get_object("entry3").set_text(ticket[1])
		self.builder.get_object("adjustment5").set_value(float(ticket[2]))
		self.builder.get_object("entry4").set_text(ticket[3])
		popup.show_all()
		
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
		self.statusPush("Database saved successfully.")

	# Save As button
	def on_toolbutton5_clicked(self, *args):
		self.db.commit()
		self.db = fileaccess.saveDialog(self.window)

	# Ticket Edit button
	def on_toolbutton6_clicked(self, *args):
		self.ticketPopup(self.ticketSelected())
	
	# Order Edit button
	def on_toolbutton7_clicked(self, *args):
		self.orderPopup(self.orderSelected())

	# Order Remove button	
	def on_toolbutton8_clicked(self, *args):
		pass

	# Order Add button
	def on_toolbutton9_clicked(self, *args):
		self.orderPopup()
		
	def on_toolbutton10_clicked(self, *args):
		self.ticketPopup()
		
	def on_toolbutton11_clicked(self, *args):
		pass
	
	def on_treeview1_row_activated(self, *args):
		print("rowactivate1", *args)
		
	def on_treeview2_row_activated(self, *args):
		print("rowactivate2", *args)
		
	def on_button2_clicked(self, *args):
		self.builder.get_object("window2").hide()
		
	def on_button4_clicked(self, *args):
		self.builder.get_object("window3").hide()

	# When called, give the value of the current selection using a unique ID
	def orderSelected(self):
		model, liststore = self.builder.get_object("treeview-selection2").get_selected()
		return str(model[liststore][0])

	def ticketSelected(self):
		model, liststore = self.builder.get_object("treeview-selection1").get_selected()
		return int(model[liststore][0])

# Create the main event loop
main = Editor()
Gtk.main()
