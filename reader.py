#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader

# Start the reader program class
class Reader():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("reader.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		self.window.show_all()

	# Fetches the text from entry1
	def textGet(self):
		entry = self.builder.get_object("entry1")
		return entry.get_text()		

	# Sets the text in entry1
	def textSet(self, text):
		entry = self.builder.get_object("entry1")
		entry.set_text(text)
		if len(self.textGet()) >= 9:
			try:
				codereader.codeRead(0, codereader.codeConv(self.textGet()))
				entry.set_text("")
			except ValueError:
				entry.set_placeholder_text("Error!")

	# Takes the existing text in entry1 and adds the character to it
	def textAdd(self, text):
		# Clear the textbox once the user starts typing again
		if self.textGet() == "Error!":
			self.textSet("")
		self.textSet(self.textGet() + text)
		
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	# Each button is linked to one definition
	def entry1_icon_press_cb(self, *args):
		self.textSet("")

	def button1_clicked_cb(self, button):
		self.textAdd("0")
		print(button)
		
	def button2_clicked_cb(self, button):
		self.textAdd("1")
		print(button)
		
	def button3_clicked_cb(self, button):
		self.textAdd("2")
		print(button)
		
	def button4_clicked_cb(self, button):
		self.textAdd("3")
		print(button)
		
	def button5_clicked_cb(self, button):
		self.textAdd("4")
		print(button)
		
	def button6_clicked_cb(self, button):
		self.textAdd("5")
		print(button)
		
	def button7_clicked_cb(self, button):
		self.textAdd("6")
		print(button)
		
	def button8_clicked_cb(self, button):
		self.textAdd("7")
		print(button)
		
	def button9_clicked_cb(self, button):
		self.textAdd("8")
		print(button)
		
	def button10_clicked_cb(self, button):
		self.textAdd("9")
		print(button)
		
	def button11_clicked_cb(self, button):
		self.textAdd("A")
		print(button)
		
	def button12_clicked_cb(self, button):
		self.textAdd("B")
		print(button)
		
	def button13_clicked_cb(self, button):
		self.textAdd("C")
		print(button)
		
	def button14_clicked_cb(self, button):
		self.textAdd("D")
		print(button)
		
	def button15_clicked_cb(self, button):
		self.textAdd("E")
		print(button)
		
	def button16_clicked_cb(self, button):
		self.textAdd("F")
		print(button)

main = Reader()
Gtk.main()
