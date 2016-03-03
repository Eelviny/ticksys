#!/usr/bin/env python3

# Code Reader Module
from checksum import sumRead
from databaseinterface import *

def codeRead(database, ticketID):
	for i in range(len(ticketID)):
		ticketID[i] = int(ticketID[i], 16)
	if not sumRead(ticketID):
		raise ValueError
	randomID = ticketID[3:7]
	runningdbs[database].read('userinfo', 'randomID={0}').format(randomID)
	# TODO: Finish databaseinterface module so this can read directly from db
	
		
def codeConv(ticketID):
	ticketList = []
	for i in ticketID:
		ticketList.append(i)
	return ticketList
