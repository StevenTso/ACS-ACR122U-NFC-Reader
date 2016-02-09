#! /usr/bin/env python
import re, argparse
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

def stringParser(dataCurr):
#--------------String Parser--------------#
	#([85, 203, 230, 191], 144, 0) -> [85, 203, 230, 191]
	if isinstance(dataCurr, tuple):
		temp = dataCurr[0]
		code = dataCurr[1]
	#[85, 203, 230, 191] -> [85, 203, 230, 191]
	else:
		temp = dataCurr
		code = 0

	dataCurr = ''

	#[85, 203, 230, 191] -> bfe6cb55 (int to hex reversed)
	for val in temp:
		# dataCurr += (hex(int(val))).lstrip('0x') # += bf
		dataCurr += format(val, '#04x')[2:] # += bf

	#bfe6cb55 -> BFE6CB55
	dataCurr = dataCurr.upper()

	#if return is successful
	if (code == 144):
		return dataCurr

def readTag(page):
		try:
			connection = reader.createConnection()
			status_connection = connection.connect()
			connection.transmit(COMMAND)
			#Read command [FF, B0, 00, page, #bytes]
			resp = connection.transmit([0xFF, 0xB0, 0x00, int(page), 0x04])
			dataCurr = stringParser(resp)

			#only allows new tags to be worked so no duplicates
			if(dataCurr is not None):
				print dataCurr
			else:
				print "Something went wrong. Page " + str(page)
		except Exception,e: print str(e)

def writeTag(page, value):
	if type(value) != str:
		print "Value input should be a string"
		exit()
	while(1):
		if len(value) == 8:
			try:
				connection = reader.createConnection()
				status_connection = connection.connect()
				connection.transmit(COMMAND)
				WRITE_COMMAND = [0xFF, 0xD6, 0x00, int(page), 0x04, int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16), int(value[6:8], 16)]
				# Let's write a page Page 9 is usually 00000000
				resp = connection.transmit(WRITE_COMMAND)
				if resp[1] == 144:
					print "Wrote " + value + " to page " + str(page)
					break
			except Exception, e:
				continue
		else:
			print "Must have a full 4 byte write value"
			break

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Read / write NFC tags')
	read_group = parser.add_argument_group('read')
	read_group.add_argument('--read', nargs='+', help='Pages to read. Can be a x-x range, or list of pages')
	write_group = parser.add_argument_group('write')
	write_group.add_argument('--write', nargs=2, metavar=('PAGE', 'DATA'), help='Page number and hex value to write.')


	args = parser.parse_args()

	#Only going to write one page at a time
	if args.write:
		page = args.write[0]
		data = args.write[1]
		if len(data) == 8:
			writeTag(int(page), data)
		else:
			raise argparse.ArgumentTypeError("Must have a full 4 byte write value")
	
	#Page numbers are sent as ints, not hex, to the reader
	if args.read:
		for page in args.read:
			if "-" in page:
				start = int(page.split("-")[0])
				end = int(page.split("-")[1])
				for new_page in xrange(start, end+1):
					readTag(new_page)
			else:
				readTag(page)
