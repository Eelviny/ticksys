#!/usr/bin/env python3

# Checksum Module

# Generate a checksum
def sumGen(ticketID):
	idno = 0
	# Multiply each value by its position, and add them together
	for i in range(7):
		idno += ticketID[i] * i+1
	hexno = format(idno, 'x')
	# Take first and last values if the hex is larger than 2 digits
	if len(hexno) > 2:
		hexno = hexno[0] + hexno[-1]
	# Return the two values as decimals in a list
	return [int(hexno[0], 16), int(hexno[1], 16)]
	
def sumRead(ticketID):
	# Work out what the actual value is
	original = sumGen(ticketID[0:7])
	# Extract the checksum of the ticketID
	actual = ticketID[7:9]
	if original == actual:
		return True
	else:
		return False
