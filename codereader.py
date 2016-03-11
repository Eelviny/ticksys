#!/usr/bin/env python3

# Code Reader Module
from checksum import sumRead
from dbinterface import *

def codeRead(database, ticketID):
	listID = codeConv(ticketID)
	if not sumRead(listID):
		raise ValueError
	return dbrunning[database].read("user_info", "code='{0}'".format(ticketID))
		
def codeConv(ticketID):
	ticketList = []
	for i in ticketID:
		ticketList.append(int(i, 16))
	return ticketList
