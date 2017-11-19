import string

data = b"\x05\x01\x00\x01"
print(data[0], "<=>", type(data[0]))    # 5 <=> <class 'int'>

"""
ord("单个的unicode字符") => Unicode编码: int类型
"""
r = ord("我")
print(r, type(r))       # 25105 <class 'int'>
r = ord("a")
print(r, type(r))       # 97 <class 'int'>

r = ord(b"\x05")
print(r, type(r))       # 5 <class 'int'>

s = str(data[0])
print(s, type(s))       # 5 <class 'str'>
r = ord(s)      # 获得字符5 的Unicode码
print(r, type(r))       # 53 <class 'int'>

b = chr(data[0]).encode("utf-8")
print(b, type(b))


# print(chr(196).encode("utf-8"))
# print(bytes((196,)))

# print("255 = ",chr(255).encode("utf-8"))
# print(bytes([255],"utf-8"))
