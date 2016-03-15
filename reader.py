#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import codereader
import dbinterface

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
		# To prevent multiple database reads, store the whole table in memory at the start
		self.tickets = dbinterface.dbrunning[database].read("ticket_types")
		print(self.tickets) # debug code

	# Fetches the text from entry1
	def textGet(self):
		return self.entry1.get_text()		

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
		print(self.textGet()) # debug code
		# The magic part of the program. Once the value is long enough, cue the info
		if len(self.textGet()) >= 9:
			try:
				# fetch the user info for the relevant code using codereader
				info = codereader.codeRead(database, self.textGet())
				print(info) # debug code
				orders = dbinterface.dbrunning[database].read("orders", "userID={0}".format(info[0][0]))
				print(orders) # debug code
				# Extract the second window
				self.popup = self.builder.get_object("window2")
				# Set the title of the second window to the code inputted, capitalised
				self.popup.set_title(self.textGet().upper())
				# Pull the users first and last names from the database and put it on the first line
				self.builder.get_object("label1").set_text(str("Name: " + info[0][1] + " " + info[0][2]))
				# The next 4 lines are for each of the 4 ticket types
				for i in range(1,5):
					# Use for loops to find the correct order number in the nested list
					order = "0"
					for a, b in enumerate(orders):
						if b[3] == i:
							order = str(b[1])
					print(order) # debug code
					# Take all the information found on the users tickets and place it into the labels
					self.builder.get_object("label{0}".format(str(i+1))).set_text(str(self.tickets[i-1][1] + ": " + order))
				# Now we have the information in place, show the user the popup box
				self.popup.show_all()
				# Reset the code reader for the next use
				self.entry1.set_text("")
			except ValueError:
				# If the checksum fails, handle gracefully and give a nice error message to the user
				self.textSet("Error!")
				self.entry1.grab_focus()
		
	# Close all windows on the deletion of the top-level window
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)
		
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
		self.popup.hide()

# For testing - Use the sample database	
dbinterface.sampleDB()
database = 0

# Create the main event loop
main = Reader()
Gtk.main()
