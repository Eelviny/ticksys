#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader
import dbinterface
import fileaccess

# Start the reader program class
class Reader():
	def __init__(self):
		# use Gtk Builder to build the UI from file
		self.builder = Gtk.Builder()
		self.builder.add_from_file("reader.glade")
		# Connect all the events to the functions in this class
		self.builder.connect_signals(self)
		# Fetch the whole window
		self.window = self.builder.get_object("window1")
		# This value needs to be changed by the program, so fetch it too
		self.entry1 = self.builder.get_object("entry1")
		# Once everything is fetched, show the windows
		self.window.show_all()
		self.db = fileaccess.openDialog(self.window)
		if self.db == None:
			raise SystemExit(0)
		# To prevent multiple database reads, store the whole table in memory at the start
		self.tickets = self.db.read("ticket_types")
		print(self.db.read("user_info"))

	# Fetches the text from entry1
	def textGet(self):
		return self.entry1.get_text().upper()	

	# Sets the text in entry1
	def textSet(self, text):
		self.entry1.set_text(text)

	# Takes the existing text in entry1 and adds the character to it
	def textAdd(self, text):
		# Clear the textbox after an error once the user starts tapping again
		if self.textGet() == "Error!":
			self.textSet("")
		self.textSet(self.textGet() + text)
		
	# Whenever the text changes, call the updater
	def textUpdate(self):
		# The magic part of the program. Once the value is long enough, cue the info
		if len(self.textGet()) >= 9:
			try:
				# Take the input and run it against the checksum
				code = self.textGet()
				codereader.codeRead(code)
				# Use dbinterface to create an easy to use list of values
				ticket = self.db.returnOrders("code='{0}'".format(code))[0]
				# Assign the popup window and set the title
				popup = self.builder.get_object("window2")
				popup.set_title(ticket[2])
				# Show the customers name at the top
				self.builder.get_object("label1").set_text("Name: " + ticket[0] + " " + ticket[1])
				# Display a row for each ticket type
				for i in range(4):
					self.builder.get_object("label{0}".format(str(i+2))).set_text(self.tickets[i][1] + ": " + str(ticket[3][i]))
				# Show the window, with all attributes set
				popup.show_all()
				# Reset the code reader for the next use
				self.entry1.set_text("")
			except:
				# If the checksum fails, handle gracefully and give a nice error message to the user
				self.textSet("Error!")
				self.entry1.grab_focus()
		
	# Close all windows on the deletion of the top-level window
	def on_window1_delete_event(self, *args):
		raise SystemExit(0)
		
	# Each button is linked to one function
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
	
	# Detect changes to entry1, and trigger the text update
	def on_entry1_changed(self, *args):
		self.textUpdate()

	# When the popup is finished with, don't destroy it - hide it away for the next use
	# The close button on the popup is disabled, so the only way to get rid of it is to use button17
	def on_button17_clicked(self, *args):
		self.builder.get_object("window2").hide()
	
	def on_filechooserbutton1_file_set(self, *args):
		pass

# Create the main event loop
main = Reader()
Gtk.main()
