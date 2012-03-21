import struct

def getItStraight(the_bytes=None, format=None):
	formats=['x','c','b','B','?','h','H','i','I','l','L','q','Q','f','d','s','p','P',]
	
	result = bytearray(the_bytes)
	result.reverse()
	if format:
		if format in formats:
			format = '!'+format
			return struct.unpack(format,result)
		else:
			return result.decode(encoding=format),
	else: return bytes(result), 
	
def stringsFromBytes(the_bytes=None, terminator=b'\x00'):
	the_strings = []
	the_bytes = bytearray(the_bytes)
	while len(the_bytes):
		the_strings.append(the_bytes[:the_bytes.index(terminator)].decode(encoding='ascii'))
		del the_bytes[:the_bytes.index(terminator)+1]
	return the_strings
