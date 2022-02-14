TLV_END = b"\xFE"
WELL_KNOWN = 0x01

# to be made dynamic later (especially with multi records support)
TNF_BYTE = 0xD1 # (MB = ME = 1, CF = 0, SR = 1, IL = 0, TNF = 0x1)

PROTOCOLS = {
    # "": b"\x00",
    "http://www.": b"\x01",
    "https://www.": b"\x02",
    "http://": b"\x03",
    "https://": b"\x04",
    "tel:": b"\x05",
    "mailto:": b"\x06",
    "ftp://anonymous:anonymous@": b"\x07",
    "ftp://ftp.": b"\x08",
    "ftps://": b"\x09",
    "sftp://": b"\x0A",
    "smb://": b"\x0B",
    "nfs://": b"\x0C",
    "ftp://": b"\x0D",
    "dav://": b"\x0E",
    "news:": b"\x0F",
    "telnet://": b"\x10",
    "imap:": b"\x11",
    "rtsp://": b"\x12",
    "urn:": b"\x13",
    "pop:": b"\x14",
    "sip:": b"\x15",
    "sips:": b"\x16",
    "tftp:": b"\x17",
    "btspp://": b"\x18",
    "btl2cap://": b"\x19",
    "btgoep://": b"\x1A",
    "tcpobex://": b"\x1B",
    "irdaobex://": b"\x1C",
    "file://": b"\x1D",
    "urn:epc:id:": b"\x1E",
    "urn:epc:tag:": b"\x1F",
    "urn:epc:pat:": b"\x20",
    "urn:epc:raw:": b"\x21",
    "urn:epc:": b"\x22",
    "urn:nfc:": b"\x23",
}

def ndef_payload(payload):
	return (
		# what is that ?
		bytes([0xE1, 0x40, 0x40, 0x05])
		# type (NDEF) and size of the TLV field
		+ bytes([0x03, len(payload)])
		+ payload
		+ TLV_END
	)

def payload_url(url):
	prefix_code = b"\x00"
	url_data = url.encode()
	# find the URL prefix for replacement
	for prefix, code in PROTOCOLS.items():
		if url.startswith(prefix):
			url_data = url[len(prefix):].encode()
			prefix_code = code
			break
	# create the payload
	url_field_length = len(url_data) + 1
	rfid_payload = (
		# record header and lengths
		bytes([TNF_BYTE, WELL_KNOWN, url_field_length])
		# URL type and prefix (https)
		+ b"U" + prefix_code
		# actual URL
		+ url_data
	)
	return ndef_payload(rfid_payload)

def payload_text(text, language='en'):
	text_data = text.encode()
	language_code = language.encode()
	type_length = len(language_code) + 1
	text_field_length = len(text_data) + type_length
	rfid_payload = (
		# record header and lengths
		bytes([TNF_BYTE, WELL_KNOWN, text_field_length])
		# text type, language length and language string
		+ b"T" + bytes([len(language_code)]) + language_code
		# actual text
		+ text_data
	)
	return ndef_payload(rfid_payload)
