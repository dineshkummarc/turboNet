import struct

WIN_EPOCH_OFFSET = 11644473600

def getItStraight(the_bytes=None, format=None):
	formats=['x','c','b','B','?','h','H','i','I','l','L','q','Q','f','d','s','p','P','24s',]
	
	result = bytearray(the_bytes)
	result.reverse()
	if format:
		if format in formats:
			format = '!'+format
			return struct.unpack(format,result)
		else:
			return result.decode(encoding=format),
	else: return bytes(result), 

def getItReversed(the_data=None, format=None):
	formats=['x','c','b','B','?','h','H','i','I','l','L','q','Q','f','d','s','p','P',]
	
	if format:
		if format in formats:
			format = '!'+format
			result = bytearray(struct.pack(format,the_data))
		else:
			result = bytearray(the_data,encoding=format)
	else: result = bytearray(the_data)
	
	result.reverse()
	return result

def string_from_bytes(bytes_=None, encoding="ascii", terminator=b'\x00'):
	bytes_ = bytearray(bytes_)
	string_ = bytes_[:bytes_.index(terminator)].decode(encoding=encoding)
	del bytes_[:bytes_.index(terminator)+1]
	return string_, bytes_

def bytes_from_string(string_=None, encoding='ascii', terminator=b'\x00'):
	bytes_ = bytearray(string_,encoding=encoding)
	bytes_.extend(bytearray(terminator))
	return bytes(bytes_)
	
	
def stringsFromBytes(the_bytes=None, terminator=b'\x00'):
	the_strings = []
	the_bytes = bytearray(the_bytes)
	while len(the_bytes):
		the_strings.append(the_bytes[:the_bytes.index(terminator)].decode(encoding='ascii'))
		del the_bytes[:the_bytes.index(terminator)+1]
	return the_strings

def bytesFromStrings(the_strings=None, terminator=b"\x00"):
	
	the_strings = list(the_strings)
	
	result = bytearray()
	for a_string in the_strings:
		result.extend(bytearray(a_string,encoding='ascii'))
		result.extend(bytearray(terminator))
		
	return result

def to_filetime(timestamp):
	return (timestamp + WIN_EPOCH_OFFSET) * 10000000
	
def from_filetime(timestamp):
	return timestamp / 10000000 - WIN_EPOCH_OFFSET