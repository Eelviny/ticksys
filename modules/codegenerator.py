# Code Generator Module
import random

def codeGen():
	randomauth = ""
	for i in range(0,4): 
		randomauth += format(random.randint(0,15), 'X')
	print(randomauth)
