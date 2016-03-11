#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codegenerator
import dbinterface

# Start the reader program class
class Creator():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("creator.glade")
		self.builder.connect_signals(self)
		self.liststore1 = Gtk.ListStore(str, str)
		self.window = self.builder.get_object("window1")
		self.entry1 = self.builder.get_object("entry1")
		self.entry2 = self.builder.get_object("entry2")
		
		self.treeview = self.builder.get_object("treeview1")
		for i, column_title in enumerate(["Ticket Type", "Price"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)

		self.treeview.set_model(self.liststore1)
		# Translate the database ticket types into a GUI list
		ticket = dbinterface.dbrunning[database].read("ticket_types")
		#self.tickets = [[str(ticket[0][1]), "£ "+str(ticket[0][2])], [str(ticket[1][1]), "£ "+str(ticket[1][2])], [str(ticket[2][1]), "£ "+str(ticket[2][2])], [str(ticket[3][1]), "£ "+str(ticket[3][2])]]
		self.tickets = []
		for i in range(4):
			self.tickets.append([ticket[i][1], str(ticket[i][2])])
			button = self.builder.get_object("button{0}".format(str(i+1)))
			button.set_label(ticket[i][1])
			button.set_tooltip_text(ticket[i][3])
		print(self.tickets)
		# The GTK list is not very useful for python usage, so create a duplicate python list alongside
		self.clearTable()
		
		self.window.show_all()
	
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	def addItem(self, ticket, price):
		liststore1.append([ticket, price])
		
	def codeSet(self, code):
		clabel = self.builder.get_object("label2")
		clabel.set_text(codegenerator.codePrint(codegenerator.codeGen(1)))
	
	def addValue(self, value):
		self.liststore1.append(self.tickets[value])
		self.ticketlist[value] += 1
		print(self.ticketlist)
		
	def clearTable(self):
		self.liststore1.clear()
		self.ticketlist = [0,0,0,0]
		self.entry1.set_text("")
		self.entry2.set_text("")
		self.code = codegenerator.codePrint(codegenerator.newCode(database))
		label2 = self.builder.get_object("label2")
		label2.set_text(str("Code: "+self.code))
		
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
		print("Open") # TODO: Link to database module
		
	def on_save_clicked(self, *args):
		fName = self.entry1.get_text()
		lName = self.entry2.get_text()
		if self.ticketlist != [0,0,0,0] and fName != "" and lName != "":
			dbinterface.dbrunning[database].newEntry(fName, lName, self.code, self.ticketlist)
			self.clearTable()
			print(dbinterface.dbrunning[database].read("user_info"))
			print(dbinterface.dbrunning[database].read("orders"))
		
# TODO: Create a file browser so it doesn't use the test database
dbinterface.sampleDB() # testing code
database = 0

main = Creator() 
Gtk.main()
