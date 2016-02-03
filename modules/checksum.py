# Checksum Module

# Generate a checksum
def sumGen(ticketID):
	idno = 0
	# Multiply each value by its position, and add them together
	for i in range(1,8):
		idno += ticketID[i] * i
	hexno = format(idno, 'x')
	# Take first and last values if the hex is larger than 2 digits
	if len(hexno) > 2:
		hexno = hexno[0] + hexno[-1]
	# Return the two values as decimals in a list
	return [int(hexno[0], 16), int(hexno[1], 16)]
	
def sumRead(ticketID):
	original = []
	# Take all except the checksum
	for i in range(8):
		original.append(ticketID[i])
	# Work out what the actual value is
	original = sumGen(original)
	# Extract the checksum of the ticketID
	actual = []
	for i in range(2):
		actual.append(i+7)
	if original == actual:
		return True
	else:
		return False
