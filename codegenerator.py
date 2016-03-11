#!/usr/bin/env python3

# Code Generator Module
import random
from checksum import *
from dbinterface import *

def randomCode():
	# Generate a 4-digit random hexadecimal string
	randomauth = []
	for i in range(0,4): 
		randomauth.append(random.randint(0,15))
	return randomauth

# The heart of the module - creating the code. If not supplied with a code, create one anyway
def codeGen(dbid, randomauth=randomCode()):
	
	# Take the inputted database ID
	dbid = str(dbid)
	dblist = []
	# If the length of dbid is shorter than 3, add zeros to the start. No values submitted will be longer than 3 characters.
	for i in range(len(dbid)):
		dblist.append(int(dbid[i]))
	while len(dblist) < 3:
		dblist = [0] + dblist
	
	# Call the checksum module to generate a valid checksum for the code
	csum = sumGen(dblist + randomauth)
	
	return dblist + randomauth + csum
	
# Take an inputted, raw code list and turn it into a human readable string
def codePrint(code):
	output = ""
	for i in range(len(code)):
		output += format(code[i], 'X')
	return output
	
def newCode():
	#TODO: Link the database module to this
	# Find the next available database ID and generate a code from it
	newid = dbRead(dbid) + 1
	return codeGen(newid)
