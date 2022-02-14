import board
import time
import adafruit_st25dv16
import rfid_payload

eeprom = adafruit_st25dv16.ST25DV16(board.I2C(), 0x53)
print(eeprom[:64])

#data = rfid_payload.make_payload("https://www.circuitpython.org/downloads")
data = rfid_payload.payload_url("http://ri1.fr")
data = rfid_payload.payload_text("Hello World !")

print(data)

# getting "unsupported operation" sometimes with this:
# eeprom[0:len(data)] = data

# write 1 byte at a time, slowly
for i in range(len(data)):
	eeprom[i] = data[i]
	time.sleep(0.01)

print(eeprom[:64])
