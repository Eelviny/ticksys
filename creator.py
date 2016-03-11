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
		
		self.treeview = self.builder.get_object("treeview1")
		for i, column_title in enumerate(["Ticket Type", "Price"]):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)

		self.treeview.set_model(self.liststore1)
		#self.treeview.set_reorderable(True)
		self.tickets = [["testing", "123"], ["Another", "456"], ["test", "453"], ["Hi there", "952"]]
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
		self.code = codegenerator.codePrint(codegenerator.newCode(0))
		
	#def newCode(self, 
		
	#def saveToDB(self, 
		
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
		entry1 = self.builder.get_object("entry1")
		entry2 = self.builder.get_object("entry2")
		fName = entry1.get_text()
		lName = entry2.get_text()
		if self.ticketlist != [0,0,0,0] and fName != "" and lName != "":
			dbinterface.dbrunning[database].newEntry(fName, lName, self.code, self.ticketlist)
			self.clearTable()
			print(dbinterface.dbrunning[database].read("user_info"))
			print(dbinterface.dbrunning[database].read("orders"))
		
# TODO: Create a file browser so it doesn't use the test database
dbinterface.newDB(":memory:") # testing code
database = 0

main = Creator() 
Gtk.main()
