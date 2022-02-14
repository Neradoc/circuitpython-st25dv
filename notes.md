Notes:
The data written in user or system memory (EEPROM), either from I2C or from RF, transits via the 256-Bytes fast transfer mode's buffer. Consequently fast transfer mode must be deactivated (MB_EN=0) before starting any write operation in user or system memory, otherwise command will be NotACK for I2C or get an answer 0Fh for RF and programming is not done.

#### NFC documentation
[https://learn.adafruit.com/adafruit-pn532-rfid-nfc/ndef](https://learn.adafruit.com/adafruit-pn532-rfid-nfc/ndef)
[https://www.oreilly.com/library/view/beginning-nfc/9781449324094/ch04.html](https://www.oreilly.com/library/view/beginning-nfc/9781449324094/ch04.html)
[NFC Data Exchange Format (NDEF).pdf](http://sweet.ua.pt/andre.zuquete/Aulas/IRFID/11-12/docs/NFC%20Data%20Exchange%20Format%20%28NDEF%29.pdf)
[https://github.com/tigoe/BeginningNFC/blob/7eb7971651f9db0b4b057769c1693fa1a948b56f/MimeWriter/platforms/android/assets/www/plugins/com.chariotsolutions.nfc.plugin/www/phonegap-nfc.js#L97-L109](https://github.com/tigoe/BeginningNFC/blob/7eb7971651f9db0b4b057769c1693fa1a948b56f/MimeWriter/platforms/android/assets/www/plugins/com.chariotsolutions.nfc.plugin/www/phonegap-nfc.js#L97-L109)


#### cf Table 11. System configuration memory map
```py
system = adafruit_24lc32.EEPROM_I2C(board.I2C(), 0x57)
print("".join([f"{x:02x} " for x in system[0:16]]))
```

#### This is the default adafruit URL that it ships with.
```py
DEFAULT = b'\xe1@@\x05\x03\x1e\xd1\x01\x1aU\x01adafruit.com/product/4701\xfe\x00'
```

#### The encoding of a Payload for NFC/RFID
```
Bit 7     6       5       4       3       2       1       0
------  ------  ------  ------  ------  ------  ------  ------ 
[ MB ]  [ ME ]  [ CF ]  [ SR ]  [ IL ]  [        TNF         ]  

[                         TYPE LENGTH                        ]

[                       PAYLOAD LENGTH                       ]

[                          ID LENGTH                         ]

[                         RECORD TYPE                        ]

[                              ID                            ]

[                           PAYLOAD                          ]
```

#### The encoding of a URI Payload
```
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
```

#### Record types
- T: Text
- U: URI
- Sp: Smart Poster
- ac: Alternative Carrier
- Hc: Handover Carrier
- Hr: Handover Request
- Hs: Handover Select

#### TNF Values
```
  TNF Value    Record Type
  ---------    -----------------------------------------
  0x00         Empty Record
               Indicates no type, id, or payload is associated with this NDEF Record.
               This record type is useful on newly formatted cards since every NDEF tag
               must have at least one NDEF Record.
               
  0x01         Well-Known Record
               Indicates the type field uses the RTD type name format.  This type name is used
               to stored any record defined by a Record Type Definition (RTD), such as storing
               RTD Text, RTD URIs, etc., and is one of the mostly frequently used and useful
               record types.
               
  0x02         MIME Media Record
               Indicates the payload is an intermediate or final chunk of a chunked NDEF Record
               
  0x03         Absolute URI Record
               Indicates the type field contains a value that follows the absolute-URI BNF
               construct defined by RFC 3986
               
  0x04         External Record
               Indicates the type field contains a value that follows the RTD external
               name specification
               
  0x05         Unknown Record
               Indicates the payload type is unknown
               
  0x06         Unchanged Record
               Indicates the payload is an intermediate or final chunk of a chunked NDEF Record
```

#### Protocol values
```
Value    Protocol
-----    --------
0x00     No prepending is done ... the entire URI is contained in the URI Field
0x01     http://www.
0x02     https://www.
0x03     http://
0x04     https://
0x05     tel:
0x06     mailto:
0x07     ftp://anonymous:anonymous@
0x08     ftp://ftp.
0x09     ftps://
0x0A     sftp://
0x0B     smb://
0x0C     nfs://
0x0D     ftp://
0x0E     dav://
0x0F     news:
0x10     telnet://
0x11     imap:
0x12     rtsp://
0x13     urn:
0x14     pop:
0x15     sip:
0x16     sips:
0x17     tftp:
0x18     btspp://
0x19     btl2cap://
0x1A     btgoep://
0x1B     tcpobex://
0x1C     irdaobex://
0x1D     file://
0x1E     urn:epc:id:
0x1F     urn:epc:tag:
0x20     urn:epc:pat:
0x21     urn:epc:raw:
0x22     urn:epc:
0x23     urn:nfc:
```

```
MISSING: how a payload is encoded on the ST25DV16.
I assume there is some prefix defining it to be used as the NFC tag or something ?
There's clearly the length there, but what are the first 5 bytes doing ?
b'\xe1@@\x05\x03'
225, 64, 64, 5, 3

Is "3" the field type (NDEF Message) from Mifare ? (it is followed by length)
0xFE is the TLV Terminator
```
