#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Reader():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("reader.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		self.window.show_all()
		
	def textSet(self, text):
		entry = self.builder.get_object("entry1")
		entry.set_text(text)
		
	def textGet(self):
		entry = self.builder.get_object("entry1")
		return entry.get_text()
		
	def textAdd(self, text):
		self.textSet(self.textGet() + text)
		
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	def entry1_icon_press_cb(self, i1, i2, i3):
		self.textSet("")
		print(i1, i2, i3)

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
