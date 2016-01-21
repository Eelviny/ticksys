# Code Generator Module
import random
from checksum import *
from databaseinterface import *

# The heart of the module - creating the code.
def codeGen(dbid):
	# Generate a 4-digit random hexadecimal string and store
	randomauth = []
	for i in range(0,4): 
		randomauth.append(random.randint(0,15))
	
	# Take the inputted database ID
	dbid = str(dbid)
	dblist = []
	# If the length of dbid is shorter than 3, add zeros to the start. No values submitted will be longer than 3 characters.
	for i in range(len(dbid))
		dblist.append(int(dbid[i]))
	while len(dblist) < 3:
		dlist = [0] + dblist
	
	# Call the checksum module to generate a valid checksum for the code
	csum = sumGen(dbid + randomauth)
	
	return dbid + randomauth + csum
	
# Take an inputted, raw code list and turn it into a human readable string
def codePrint(code):
	output = ""
	for i in range(len(code)):
		output += format(code[i], 'X')
	return output
	

