import socketserver
import struct
import random
import os.path

import net.utils

HOST, PORT = "127.0.0.1", 6112
RCV_BUFFER_LENGTH = 2048
OUTPUT_BUFFER_LENGTH = 1460

verbose=True
debug=True

internal_protocol = None
transfer = None

def send_file_v1(file_name, trasfer_position=0):
	
	staticAnswer = [(24 + len(file_name) + 1, "H"),										#header length
					(0,	"H"),														#Unknown 
					(int(os.path.getsize(file_name)), "I"),							#file size
					(0, "I"),														#banners id
					(0, "I"),														#banners file ext
					(net.utils.to_filetime(int(os.path.getmtime(file_name))), "Q"),	#remote file time
					(file_name,	None),												#file name
					]
	
	print("answ",staticAnswer,sep=" : ",end='\n')
	
	response = bytearray()
	for field in staticAnswer:
		value, format = field
		if format:
			response.extend(net.utils.getItReversed(the_data=value, format=format))
		else:
			response.extend(net.utils.bytes_from_string(string_ = value))
	
	# file = open(file_name,mode="br")
	# file.seek(trasfer_position)
	# response.extend(file.read(OUTPUT_BUFFER_LENGTH))
	# trasfer_position = OUTPUT_BUFFER_LENGTH
	
	print('sending',response,sep='<-',end="\n")
	
	return response, trasfer_position

def resume_send_file_v1(file_name, trasfer_position=0):
	print("resuming transfer")
	file = open(file_name, mode="br")
	file.seek(trasfer_position)
	try:
		data = file.read(OUTPUT_BUFFER_LENGTH)
	except TypeError:
		pass
	trasfer_position += OUTPUT_BUFFER_LENGTH
	return data, trasfer_position
	
def server_50(request):

	messageType = net.utils.getItReversed(0x50,'B')
	staticAnswer = b'\xff\x50\xe5\x00\x02\x00\x00\x00\xb2\x08\xa9\x4d\x01\x00\x00\x00\x00\x74\xeb\xf7\x42\xe1\xc3\x01\x49\x58\x38\x36\x76\x65\x72\x31\x2e\x6d\x70\x71\x00\x41\x3d\x33\x38\x34\x35\x35\x38\x31\x36\x33\x34\x20\x42\x3d\x38\x38\x30\x38\x32\x33\x35\x38\x30\x20\x43\x3d\x31\x33\x36\x33\x39\x33\x37\x31\x30\x33\x20\x34\x20\x41\x3d\x41\x2d\x53\x20\x42\x3d\x42\x2d\x43\x20\x43\x3d\x43\x2d\x41\x20\x41\x3d\x41\x2d\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
	
	equation = "A=2521522835 B=3428392135 C=218673704 4 A=A^S B=B-C C=C+A A=A-B" #Starcraft Broodwar
	mpqfilename = 'ver-ix86-1.mpq'
	sessionkey = random.randint(0,4294967295)
	print(sessionkey)
	timestamp = net.utils.to_filetime(int(os.path.getmtime(mpqfilename)))
	
	staticAnswer = [(0, "B"),			#unknown byte
					(0,	"I"),			#logontype
					(sessionkey, "L"),	#sessionkey
					(0, "I"),			#sessionnum
					(timestamp, "Q"),	#timestamp
					mpqfilename,		#versioncheck filename
					equation,			#equation
					]
	
	print(staticAnswer)
	
	mpqfn = staticAnswer.pop(5)
	eqn = staticAnswer.pop(5)
	
	for i in range(len(staticAnswer)):
		staticAnswer[i] = net.utils.getItReversed(*staticAnswer[i])
	
	print(staticAnswer)
	messageTail = net.utils.bytesFromStrings(the_strings = (mpqfn, eqn))
	
	theAnswer = bytearray()
	for answer in staticAnswer:
		theAnswer.extend(bytearray(answer))
	
	theAnswer.extend(messageTail)
	messageSize = net.utils.getItReversed(len(theAnswer)+3,'B')
	
	messageOpen = net.utils.getItReversed(0xff,'B')
	
	# theAnswer.insert(0,messageHeader)
	messageHeader = bytearray(messageOpen)
	messageHeader.extend(messageType)
	messageHeader.extend(messageSize)
	messageHeader.extend(theAnswer)
	
	print("answ",messageHeader,sep="<-",end='\n')
	
	request.send(messageHeader)

def server_51():
	messageType = net.utils.getItReversed
	
	staticAnswer = [(0xff, 'B'),		#chat message
					(0x51, 'B'),		#message type
					(15, "B"),			#header length
					(0,	"I"),			#response code
					("nothing",	None),	#description
					]
	
	print("answ",staticAnswer,sep=" : ",end='\n')
	
	response = bytearray()
	for field in staticAnswer:
		value, format = field
		if format:
			response.extend(net.utils.getItReversed(the_data=value, format=format))
		else:
			response.extend(net.utils.bytes_from_string(string_ = value))
			
	print('sending',response,sep='<-',end="\n")
	
	return response
	
def server_25(request):	
	
	teststring = (0xff,0x25,10,210,12,54,154,53,243,234,124)
	
	message = struct.pack('!BBBBBBBBBBB',*teststring)
	
	print('sending',message,sep='<-',end="\n")
	
	request.send(message)

class tcpHandle(socketserver.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

	def handle(self):
		
		while True:
			self.message = self.request.recv(RCV_BUFFER_LENGTH)
			self.message_length = len(self.message)
			
			if hasattr(self,"internal_protocol"): print("using protocol",self.internal_protocol)
			else: print("there is no protocol defined")
			
			if debug:
				print('getting',self.message_length,'bytes',sep=' ',end='\n')
				print(self.client_address[0],self.message,sep='<-',end='\n')
			
			# Detecting message type
			if self.message_length is 0:
				package_leading_byte = None
			elif self.message_length is 1:
				package_leading_byte = list(struct.unpack('!B',self.message))
				if not hasattr(self,"internal_protocol"):
					self.internal_protocol = package_leading_byte[0]
			else:
				if not hasattr(self,"internal_protocol"):
					package_leading_byte = list(struct.unpack('!B' + str(self.message_length - 1) + 's', self.message))
					self.internal_protocol = package_leading_byte[0]
					self.message = self.message[1:]
					self.message_length = len(self.message)
				
				package_leading_byte = list(struct.unpack('!B' + str(self.message_length - 1) + 's', self.message))
			
			if not hasattr(self,"internal_protocol"):
				if debug:
					print('mode',self.internal_protocol,sep=' : ',end='\n')
			
			if self.internal_protocol is 1:
				
				if package_leading_byte[0] is 255:
					messageHead = struct.unpack('!B2s'+str(len(package_leading_byte[1])-3)+'s',package_leading_byte[1])
					messageHead = list(messageHead)
					messageHead[1], = net.utils.getItStraight(messageHead[1],'H')
					
					if debug:
						print('message header',*messageHead,sep=' : ',end='\n')
						if messageHead[1] is not self.message_length:
							print('size header MISMATCH!!!!!',end='\n')
					
					if messageHead[0] is 80:
					
						names = ['protocol','archtag','clienttag','versionid','gamelang','localip','bias','lcid','langid','langstr','countryname']
						
						messageContent = struct.unpack('!4s4s4s4s4s4s4s4s4s'+str(len(messageHead[2])-36)+'s',messageHead[2])
						messageContent = list(messageContent)
						
						ipnat = struct.unpack('!BBBB',messageContent.pop(5))
						format=['I','ascii','ascii','I','ascii','i','I','I']
						for i in range(8):
							messageContent[i], = net.utils.getItStraight(the_bytes=messageContent[i],format=format[i])
						
						messageContent[5] = struct.pack('B',messageContent[5])
						messageContent[5], = struct.unpack('b',messageContent[5])
						messageContent.insert(5,ipnat)
						a_string = messageContent.pop(9)
						messageContent.extend(net.utils.stringsFromBytes(the_bytes=a_string))
						
						messageContent = dict(zip(names, messageContent))
						
						if debug:
							print('message content',messageContent,sep=' : ',end='\n')
						
						server_50(self.request)
					
					if messageHead[0] is 81:
						contentFormat = [('client_token', 'I'),
										('executable_version', 'I'),
										('executable_hash', 'I'),
										('key_count', 'I'),
										('spawn', 'I'),
										('key_length', 'I'),
										('product_value', 'I'),
										('public_value', 'I'),
										('unknown1', 'I'),
										('hashed_data', '24s'),
										('executable_info', None),
										('owner_name', None),
										]
						
						message_content = struct.unpack('!4s4s4s4s4s4s4s4s4s24s'+str(self.message_length-60)+'s',self.message)
						message_content = list(message_content)
						
						content = {}
						
						for i in range(len(message_content)):
							name, format = contentFormat[i]
							if format: content[name], = net.utils.getItStraight(the_bytes=message_content[i],format=format)
							else:
								string_in_bytes = message_content[i]
								while string_in_bytes:
									name, format = contentFormat[i]
									content[name], string_in_bytes = net.utils.string_from_bytes(bytes_=string_in_bytes)
									i += 1
						
						print('content',content, sep=' : ')
						
						self.request.send(server_51())
					
					if messageHead[0] is 37:
						
						names = ['bytes']
						
						messageContent,  = net.utils.getItStraight(format='I', the_bytes=messageHead[2])
						messageContent = dict(zip(names, messageContent))
						
						if debug:
							print('message content',messageContent,sep=' : ',end='\n')
						
						
						
						staticAnswer = b'\xff\x25\x08\x00\x4f\xe1\x1c\x00'
						
						server_25(self.request)
						
			if self.internal_protocol is 2:
				
				if debug:
					print("startFTP")
				
				if not hasattr(self,"transfer"):
					
					
					if self.message_length > 1:
						
						self.empty_messages = 0
						
						contentFormat = [('message_length', 'H'),
										('protocol_ver', 'H'),
										('platform_id', 'ascii'),
										('product_id', 'ascii'),
										('banner_id', 'I'),
										('banner_ext', 'I'),
										('file_offset', 'I'),
										('file_mod_time', 'Q'),
										('file_name', None),
										]
						
						message_content = struct.unpack('!2s2s4s4s4s4s4s8s'+str(self.message_length-32)+'s',self.message)
						message_content = list(message_content)
						
						# message_text = message_content.pop(8)
						content = {}
						
						for i in range(len(message_content)):
							name, format = contentFormat[i]
							if format: content[name], = net.utils.getItStraight(the_bytes=message_content[i],format=format)
							else:
								string_in_bytes = message_content[i]
								while string_in_bytes:
									name, format = contentFormat[i]
									content[name], string_in_bytes = net.utils.string_from_bytes(bytes_=string_in_bytes)
									i += 1
									
						content['file_mod_time'] = net.utils.from_filetime(content['file_mod_time'])
						# content["file_name"] = net.utils.stringsFromBytes(the_bytes=message_text)
						
						print('FTP -> ',content, sep=' : ')
						
						if content['message_length'] is not self.message_length:
							print('size header MISMATCH!!!!!',end='\n')
							
						self.transfer = content['file_name']
						
						response, self.trasfer_position = send_file_v1(content['file_name'])
						self.request.send(response)
						
						while self.trasfer_position < int(os.path.getsize(content['file_name'])):
							print("sending from",self.trasfer_position,"to",self.trasfer_position + OUTPUT_BUFFER_LENGTH,sep=" ")
							data, self.trasfer_position = resume_send_file_v1(content['file_name'], trasfer_position=self.trasfer_position)
							self.request.send(data)
						
						
					else:
						if not hasattr(self,"empty_messages"):
							self.empty_messages = 0
						
						self.empty_messages += 1
						print("empty message", self.empty_messages, sep=" ")
					
						if self.empty_messages > 3:
							self.request.close()
						
				else:
					if self.trasfer_position < int(os.path.getsize(self.transfer)):
						print("sending from",self.trasfer_position,"to",self.trasfer_position + OUTPUT_BUFFER_LENGTH,sep=" ")
						data, self.trasfer_position = resume_send_file_v1(self.transfer, trasfer_position=self.trasfer_position)
						self.request.send(data)
					else:
						self.request.close()
				

					
					
				
				
					
						

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
				
def start():
	
	# Create the server
	server = ThreadedTCPServer((HOST, PORT), tcpHandle)
	
	server.serve_forever()

if __name__ == "__main__":
	
	# registerParsers()
	# registerServers()
	# populateEnabled()
	start()
	# testing = struct.pack('!B',0x50)
	# print(testing)
	