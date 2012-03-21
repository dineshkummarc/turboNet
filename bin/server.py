import socketserver
import struct
import net.utils

HOST, PORT = "localhost", 6112
RCV_BUFFER_LENGTH=512

verbose=True
debug=True

protocolMode = None



class tcp(socketserver.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

	def handle(self):
		
		global protocolMode
		
		while True:
			self.rcv_pack=self.request.recv(RCV_BUFFER_LENGTH)
			messageLength = len(self.rcv_pack)
			
			if debug:
				print('getting',messageLength,'bytes',sep=' ',end='\n')
				print(self.client_address[0],self.rcv_pack,sep='<-',end='\n')
			
			# Detecting message type
			if messageLength is 0:
				packageHeadArea = None
			elif messageLength is 1:
				packageHeadArea = struct.unpack('!B',self.rcv_pack)
			else:
				packageHeadArea = struct.unpack('!B'+str(len(self.rcv_pack)-1)+'s',self.rcv_pack)
			
			if debug:
				print('command type',*packageHeadArea,sep=' : ',end='\n')
			
			packageHeadArea = list(packageHeadArea)
			
			if (protocolMode is not packageHeadArea[0]) and (packageHeadArea[0] is not 255):
				protocolMode = packageHeadArea[0]
				if debug:
					print('mode',protocolMode,sep=' : ',end='\n')
				if messageLength > 1:
					print('algo\n')
			
			if packageHeadArea[0] is 255:
				messageHead = struct.unpack('!B2s'+str(len(packageHeadArea[1])-3)+'s',packageHeadArea[1])
				messageHead = list(messageHead)
				messageHead[1], = net.utils.getItStraight(messageHead[1],'H')
				
				if debug:
					print('message header',*messageHead,sep=' : ',end='\n')
					if messageHead[1] is not messageLength:
						print('size header MISMATCH!!!!!',end='\n')
				
				if messageHead[0] is 80:
				
					names = ['protocol','archtag','clienttag','versionid','gamelang','localip','bias','lcid','langid','langstr','countryname']
					
					messageContent = struct.unpack('!4s4s4s4s4s4s4s4s4s'+str(len(messageHead[2])-36)+'s',messageHead[2])
					messageContent = list(messageContent)
					
					ipnat = struct.unpack('!BBBB',messageContent.pop(5))
					format=['I','ascii','ascii','I','ascii','i','I','I']
					for i in range(8):
						messageContent[i], = net.utils.getItStraight(the_bytes=messageContent[i],format=format[i])
					
					messageContent.insert(5,ipnat)
					a_string = messageContent.pop(9)
					messageContent.extend(net.utils.stringsFromBytes(the_bytes=a_string))
					
					if debug:
						print('message content',*messageContent,sep=' : ',end='\n')
					
					
					staticAnswer = b'\xff\x50\xe5\x00\x02\x00\x00\x00\xb2\x08\xa9\x4d\x01\x00\x00\x00\x00\x74\xeb\xf7\x42\xe1\xc3\x01\x49\x58\x38\x36\x76\x65\x72\x31\x2e\x6d\x70\x71\x00\x41\x3d\x33\x38\x34\x35\x35\x38\x31\x36\x33\x34\x20\x42\x3d\x38\x38\x30\x38\x32\x33\x35\x38\x30\x20\x43\x3d\x31\x33\x36\x33\x39\x33\x37\x31\x30\x33\x20\x34\x20\x41\x3d\x41\x2d\x53\x20\x42\x3d\x42\x2d\x43\x20\x43\x3d\x43\x2d\x41\x20\x41\x3d\x41\x2d\x42\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
					
					staticAnswer = b'\xff\x25\x08\x00\x4f\xe1\x1c\x00'
					
					self.request.send(staticAnswer)

def start():
	
	# Create the server
	server = socketserver.TCPServer((HOST, PORT), tcp)
	
	server.serve_forever()

if __name__ == "__main__":
	
	# registerParsers()
	# registerServers()
	# populateEnabled()
	start()