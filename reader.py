#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader
import dbinterface

# Start the reader program class
class Reader():
	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("reader.glade")
		self.builder.connect_signals(self)
		self.window = self.builder.get_object("window1")
		self.entry1 = self.builder.get_object("entry1")
		self.window.show_all()
		self.tickets = dbinterface.dbrunning[0].read("ticket_types")
		print(self.tickets)

	# Fetches the text from entry1
	def textGet(self):
		return self.entry1.get_text()		

	# Sets the text in entry1
	def textSet(self, text):
		self.entry1.set_text(text)
		if len(self.textGet()) >= 9:
			try:
				info = codereader.codeRead(0, self.textGet())
				print(info)
				orders = dbinterface.dbrunning[0].read("orders", "userID={0}".format(info[0][0]))
				print(orders)
				self.popup = self.builder.get_object("window2")
				self.popup.set_title(self.textGet())
				self.builder.get_object("label1").set_text(str("Name: " + info[0][1] + " " + info[0][2]))
				for i in range(2,6):
					# Use loops to find the correct order number
					order = "0"
					for a, b in enumerate(orders):
						if b[3] == i:
							order = str(b[1])
					print(order)
					self.builder.get_object("label{0}".format(str(i))).set_text(str(self.tickets[i-2][1] + ": " + order))
				self.popup.show_all()
				self.entry1.set_text("")
			except ValueError:
				self.entry1.set_text("Error!")

	# Takes the existing text in entry1 and adds the character to it
	def textAdd(self, text):
		# Clear the textbox once the user starts typing again
		if self.textGet() == "Error!":
			self.textSet("")
		self.textSet(self.textGet() + text)
		
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
	# Each button is linked to one definition
	def on_entry1_icon_press(self, *args):
		self.textSet("")

	def on_button1_clicked(self, *args):
		self.textAdd("0")
		
	def on_button2_clicked(self, *args):
		self.textAdd("1")
		
	def on_button3_clicked(self, *args):
		self.textAdd("2")
		
	def on_button4_clicked(self, *args):
		self.textAdd("3")
		print(button)
		
	def on_button5_clicked(self, *args):
		self.textAdd("4")
		
	def on_button6_clicked(self, *args):
		self.textAdd("5")
		
	def on_button7_clicked(self, *args):
		self.textAdd("6")
		
	def on_button8_clicked(self, *args):
		self.textAdd("7")
		
	def on_button9_clicked(self, *args):
		self.textAdd("8")
		
	def on_button10_clicked(self, *args):
		self.textAdd("9")
		
	def on_button11_clicked(self, *args):
		self.textAdd("A")
		
	def on_button12_clicked(self, *args):
		self.textAdd("B")
		
	def on_button13_clicked(self, *args):
		self.textAdd("C")
		
	def on_button14_clicked(self, *args):
		self.textAdd("D")
		
	def on_button15_clicked(self, *args):
		self.textAdd("E")
		
	def on_button16_clicked(self, *args):
		self.textAdd("F")
		
	def on_button17_clicked(self, *args):
		self.popup.hide()

	def on_window2_delete_event(self, *args):
		self.popup.hide()
		
dbinterface.sampleDB()
main = Reader()
Gtk.main()
