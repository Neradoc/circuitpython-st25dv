"""
Notes:
The data written in user or system memory (EEPROM), either from I2C or from RF, transits via the 256-Bytes fast transfer mode's buffer. Consequently fast transfer mode must be deactivated (MB_EN=0) before starting any write operation in user or system memory, otherwise command will be NotACK for I2C or get an answer 0Fh for RF and programming is not done.
"""

import board
import time
import adafruit_24lc32

eeprom = adafruit_24lc32.EEPROM_I2C(board.I2C(), 0x53)
print(eeprom[:38])

""" cf Table 11. System configuration memory map """
# system = adafruit_24lc32.EEPROM_I2C(board.I2C(), 0x57)
# print("".join([f"{x:02x} " for x in system[0:16]]))


"""
This is the default adafruit URL that it ships with.
b'\xe1@@\x05\x03\x1e\xd1\x01\x1aU\x01adafruit.com/product/4701\xfe\x00'
"""
DEFAULT = b'\xe1@@\x05\x03\x1e'+b'\xd1\x01\x1aU\x01adafruit.com/product/4701'+b'\xfe'

"""
https://learn.adafruit.com/adafruit-pn532-rfid-nfc/ndef
The encoding of a URL for NFC/RFID
+-------------------------+----------------------------------------------------------------
| D1                      | Record header (MB = ME = 1, CF = 0, SR = 1, IL = 0, TNF = 0x1)
+-------------------------+----------------------------------------------------------------
| 01                      | Type Length (1 byte)
+-------------------------+----------------------------------------------------------------
| 0B                      | Payload Length (11 bytes)
+-------------------------+----------------------------------------------------------------
| 55                      | Type Name ("U")
+-------------------------+----------------------------------------------------------------
| 02 67 6F 6F 67 6C 65 2E | Payload: Identifier code = 2 (prefix "https://www."),
| 63 6F 6D                |          truncated URI = "google.com"
+-------------------------+----------------------------------------------------------------
"""

"""
MISSING: how a payload is encoded on the ST25DV16.
I assume there is some prefix defining it to be used as the NFC tag or something ?
There's clearly the length there, but what are the first 5 bytes doing ?
b'\xe1@@\x05\x03'
225, 64, 64, 5, 3
it also end with FE.

Is "3" the field type (NDEF Message) from Mifare ? (it is followed by length)
0xFE is the TLV Terminator
"""

TLV_END = b"\xFE"

def make_payload(url):
	url_data = url.encode()
	rfid_payload = (b""
		# record header and lengths
		+ bytes([0xD1, 1, len(url_data)+1])
		# URL type and prefix (https)
		+ b"U" + b"\x02"
		# actual URL
		+ url_data
	)
	return (b""
		# what is that ?
		+ bytes([0xE1, 0x40, 0x40, 0x05])
		# type (NDEF) and size of the TLV field
		+ bytes([0x03, len(rfid_payload)])
		+ rfid_payload
		+ TLV_END
	)

data = make_payload("circuitpython.org/downloads")
# data = DEFAULT

# getting "unsupported operation" sometimes with this:
# eeprom[0:len(data)] = data

# write 1 byte at a time, slowly
for i in range(len(data)):
	eeprom[i] = data[i]
	time.sleep(0.01)

print(eeprom[:48])
