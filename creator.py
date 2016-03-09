#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader

# Start the reader program class
class Reader():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("creator.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		self.window.show_all()

main = Reader()
Gtk.main()
