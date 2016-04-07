#!/usr/bin/env python3

# Code Reader Module
from checksum import sumRead
from dbinterface import *

# Find the corresponding database record by submitting a query
def codeRead(ticketID):
	listID = codeConv(ticketID)
	# Check the checksum first before continuing onto the database
	if not sumRead(listID):
		raise ValueError
		
# Take a human-readable code and turn it into an integer list for the checksum generator
def codeConv(ticketID):
	ticketList = []
	for i in ticketID:
		ticketList.append(int(i, 16))
	return ticketList
