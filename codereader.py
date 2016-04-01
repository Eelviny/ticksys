#!/usr/bin/env python3

# Code Reader Module
from checksum import sumRead
from dbinterface import *

# Find the corresponding database record by submitting a query
def codeRead(db, ticketID):
	listID = codeConv(ticketID)
	# Check the checksum first before continuing onto the database
	if not sumRead(listID):
		raise ValueError
	# Return the database record containing the ticket code
	return db.read("user_info", "code='{0}'".format(ticketID.upper()))
		
# Take a human-readable code and turn it into an integer list for the checksum generator
def codeConv(ticketID):
	ticketList = []
	for i in ticketID:
		ticketList.append(int(i, 16))
	return ticketList
