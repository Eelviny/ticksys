#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader

# Start the reader program class
class Creator():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("creator.glade")
		self.builder.connect_signals(self)
		self.liststore1 = Gtk.ListStore(str, str)
		self.window = self.builder.get_object("window1")
		print(self.builder.get_objects()) # debug code
		
		self.treeview = self.builder.get_object("treeview1")
		self.cell0 = Gtk.CellRendererText()
		self.col0 = Gtk.TreeViewColumn("Ticket Type", self.cell0, text=0)
		self.col1 = Gtk.TreeViewColumn("Price", self.cell0, text=0)
		self.treeview.append_column(self.col0)
		self.treeview.append_column(self.col1)
		self.treeview.set_model(self.liststore1)
		#self.treeview.set_reorderable(True)
		
		self.window.show_all()
	
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	def addItem(ticket, price):
		liststore1.append([ticket, price])
		

main = Creator()
Gtk.main()
