#! /usr/bin/env python
import re
from smartcard.System import readers
import datetime

#ACS ACR122U NFC Reader
#Suprisingly, to get data from the tag, it is a handshake protocol
#You send it a command to get data back
#This command below is based on the "API Driver Manual of ACR122U NFC Contactless Smart Card Reader"
COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00] #handshake cmd needed to initiate data transfer

# get all the available readers
r = readers()
print "Available readers:", r

reader = r[0]
print "Using:", reader

#data from NFC tag
data = ''

while(1):
	try:
		connection = reader.createConnection()
		status_connection = connection.connect()
		dataCurr = connection.transmit(COMMAND)

		#--------------String Parser--------------#
		#([85, 203, 230, 191], 144, 0) -> [85, 203, 230, 191]
		if isinstance(dataCurr, tuple):
			temp = dataCurr[0]
		#[85, 203, 230, 191] -> [85, 203, 230, 191]
		else:
			temp = dataCurr

		dataCurr = ''

		#[85, 203, 230, 191] -> bfe6cb55 (int to hex reversed)
		for val in temp:
			# dataCurr += (hex(int(val))).lstrip('0x') # += bf
			dataCurr += format(val, '#04x')[2:] # += bf

		#bfe6cb55 -> BFE6CB55
		dataCurr = dataCurr.upper()

		#only allows new tags to be worked so no duplicates
		if(dataCurr != data):
			data = dataCurr

	except Exception, e:
		continue