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
		self.liststore1.append(["test1", "test2"])
		self.liststore1.append(["test3", "test4"])
		self.liststore1.append(["test5", "test6"])
		self.window = self.builder.get_object("window1")
		print(self.builder.get_objects()) # debug code
		
		self.treeview = self.builder.get_object("treeview1")
		self.C_DATA_COLUMN_NUMBER_IN_MODEL = 0
		self.cell0 = Gtk.CellRendererText()
		self.col0 = Gtk.TreeViewColumn("title", self.cell0, text=self.C_DATA_COLUMN_NUMBER_IN_MODEL)
		self.col1 = Gtk.TreeViewColumn("title2", self.cell0, text=self.C_DATA_COLUMN_NUMBER_IN_MODEL)
		self.treeview.append_column(self.col0)
		self.treeview.append_column(self.col1)

		self.treeview.set_model(self.liststore1)
		self.treeview.set_reorderable(True)
		
		self.window.show_all()
		

main = Creator()
Gtk.main()
