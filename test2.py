#!/usr/bin/env python3

from pirc522 import RFID
rdr = RFID(pin_ce=0, antenna_gain = 7)

while True:
	# rdr.wait_for_tag()
	# print(rdr.read(0))
	uid=rdr.read_id(as_number = True)
	if uid is not None:
		print(f'UID: {uid:X}')

reader.cleanup()
