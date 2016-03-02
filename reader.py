import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Reader():
	def __init__(self):
		builder = Gtk.Builder()
		builder.add_from_file("reader.glade")
		builder.connect_signals(self)
		window = builder.get_object("window1")
		window.show_all()
		
	def onDeleteWindow(self, *args):
			Gtk.main_quit(*args)

	def onButtonPressed(self, button):
    		print("Hello World!")

main = Reader()
Gtk.main()
