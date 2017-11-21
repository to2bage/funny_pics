import re

# 

data = b"\x05\x01\x00\x03\x0btwitter.com\x01\xbb"
print(len(data))

print(data.startswith(b"\x05"))

data = b"\x05\x01\x00"

#print(data[4])      # out of range
print(len(data))

# b"0x05 0x01 0x00 0x01 0x7f 0x00 0x00 0x01 0x1f 0x40
data = b"\x05\x01\x00\x01\x7f\x00\x00\x01\x1f\x40"
print(data[-2:])
d = b"\x1f\x40"
print(d)