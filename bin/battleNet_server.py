import socketserver
import os

#Do the same trick {try: ..... except ImportError:...}
try:
	import console
except ImportError:
	from battleNet import console

HOST, PORT = "localhost", 6112
RCV_BUFFER_LENGTH=1024

debug=True
verbose=True
quiet=False

if quiet:
	debug=false
	verbose=false
console.debug=debug
console.verbose=verbose
console.quiet=quiet
	
	
enable=['star','sexp']

parsers={}
servers={}
enabled=[]

requirements={	'star':(['common','bnc'],['sexp']),
				'sexp':(['common','bnc'],['sexp'])
			}

try:
	from net import common
	parsers['common']=common
	console.Debug('common parser 1st import succedded')
except ImportError as err:
	console.Exception('common parser 1st import failed',err)
	try:
		from battleNet.net import common
		parsers['common']=common
		console.Debug('common parser 2nd import succedded')
	except ImportError as err:
		console.Exception('common parser 2nd import failed',err)
		console.Description('common parser error or not found')
state= 'common' in parsers
console.likeBoot('common parser',state)
	
try:
	from net import bnc
	parsers['bnc']=bnc
	console.Debug('bnc parser 1st import succedded')
except ImportError as err:
	console.Exception('bnc parser 1st import failed',err)
	try:
		from battleNet.net import bnc
		parsers['bnc']=bnc
		console.Debug('bnc parser 2nd import succedded')
	except ImportError as err:
		console.Exception('bnc parser 2nd import failed',err)
		console.Description('bnc parser error or not found')
state= 'bnc' in parsers
console.likeBoot('bnc parser',state)

try:
	from net import mcp
	parsers['mcp']=mcp
	console.Debug('mcp parser 1st import succedded')
except ImportError as err:
	console.Exception('mcp parser 1st import failed',err)
	try:
		from battleNet.net import mcp
		parsers['mcp']=mcp
		console.Debug('mcp parser 2nd import succedded')
	except ImportError as err:
		console.Exception('mcp parser 2nd import failed',err)
		console.Description('mcp parser error or not found')
state= 'mcp' in parsers
console.likeBoot('mcp parser',state)

try:
	from net import d2g
	parsers['d2g']=d2g
	console.Debug('d2g parser 1st import succedded')
except ImportError as err:
	console.Exception('d2g parser 1st import failed',err)
	try:
		from battleNet.net import d2g
		parsers['d2g']=d2g
		console.Debug('d2g parser 2nd import succedded')
	except ImportError as err:
		console.Exception('d2g parser 2nd import failed',err)
		console.Description('d2g parser error or not found')
state= 'd2g' in parsers
console.likeBoot('d2g parser',state)

try:
	from net import bnp
	parsers['bnp']=bnp
	console.Debug('bnp parser 1st import succedded')
except ImportError as err:
	console.Exception('bnp parser 1st import failed',err)
	try:
		from battleNet.net import bnp
		parsers['bnp']=bnp
		console.Debug('bnp parser 2nd import succedded')
	except ImportError as err:
		console.Exception('bnp parser 2nd import failed',err)
		console.Description('bnp parser error or not found')
state= 'bnp' in parsers
console.likeBoot('bnp parser',state)

try:
	from net import bnl
	parsers['bnl']=bnl
	console.Debug('bnl parser 1st import succedded')
except ImportError as err:
	console.Exception('bnl parser 1st import failed',err)
	try:
		from battleNet.net import bnl
		parsers['bnl']=bnl
		console.Debug('bnl parser 2nd import succedded')
	except ImportError as err:
		console.Exception('bnl parser 2nd import failed',err)
		console.Description('bnl parser error or not found')
state= 'bnl' in parsers
console.likeBoot('bnl parser',state)

try:
	from net import w3g
	parsers['w3g']=w3g
	console.Debug('w3g parser 1st import succedded')
except ImportError as err:
	console.Exception('w3g parser 1st import failed',err)
	try:
		from battleNet.net import w3g
		parsers['w3g']=w3g
		console.Debug('w3g parser 2nd import succedded')
	except ImportError as err:
		console.Exception('w3g parser 2nd import failed',err)
		console.Description('w3g parser error or not found')
state= 'w3g' in parsers
console.likeBoot('w3g parser',state)

try:
	from net import stm
	parsers['stm']=stm
	console.Debug('stm parser 1st import succedded')
except ImportError as err:
	console.Exception('stm parser 1st import failed',err)
	try:
		from battleNet.net import stm
		parsers['stm']=stm
		console.Debug('stm parser 2nd import succedded')
	except ImportError as err:
		console.Exception('stm parser 2nd import failed',err)
		console.Description('stm parser error or not found')
state= 'stm' in parsers
console.likeBoot('stm parser',state)

try:
	from servers import w2bn
	servers['w2bn']=w2bn
	console.Debug('W2BN server 1st import succedded')
except ImportError as err:
	console.Exception('W2BN server 1st import failed',err)
	try:
		from battleNet.servers import w2bn
		servers['w2bn']=w2bn
		console.Debug('W2BN server 2nd import succedded')
	except ImportError as err:
		console.Exception('W2BN server 2nd import failed',err)
		console.Description('W2BN server error or not found')
state= 'w2bn' in servers
console.likeBoot('W2BN server',state)

try:
	from servers import drtl
	servers['drtl']=drtl
	console.Debug('DRTL server 1st import succedded')
except ImportError as err:
	console.Exception('DRTL server 1st import failed',err)
	try:
		from battleNet.servers import drtl
		servers['drtl']=drtl
		console.Debug('DRTL server 2nd import succedded')
	except ImportError as err:
		console.Exception('DRTL server 2nd import failed',err)
		console.Description('DRTL server error or not found')
state= 'drtl' in servers
console.likeBoot('DRTL server',state)
		
try:
	from servers import sexp
	servers['sexp']=sexp
	console.Debug('SEXP server 1st import succedded')
except ImportError as err:
	console.Exception('SEXP server 1st import failed',err)
	try:
		from battleNet.servers import sexp
		servers['sexp']=sexp
		console.Debug('SEXP server 2nd import succedded')
	except ImportError as err:
		console.Exception('SEXP server 2nd import failed',err)
		console.Description('SEXP server error or not found')
state= 'sexp' in servers
console.likeBoot('SEXP server',state)

try:
	from servers import w3xp
	servers['w3xp']=w3xp
	console.Debug('W3XP server 1st import succedded')
except ImportError as err:
	console.Exception('W3XP server 1st import failed',err)
	try:
		from battleNet.servers import w3xp
		servers['w3xp']=w3xp
		console.Debug('W3XP server 2nd import succedded')
	except ImportError as err:
		console.Exception('W3XP server 2nd import failed',err)
		console.Description('W3XP server error or not found')
state= 'w3xp' in servers
console.likeBoot('W3XP server',state)

try:
	from servers import d2xp
	servers['d2xp']=d2xp
	console.Debug('D2XP server 1st import succedded')
except ImportError as err:
	console.Exception('D2XP server 1st import failed',err)
	try:
		from battleNet.servers import d2xp
		servers['d2xp']=d2xp
		console.Debug('D2XP server 2nd import succedded')
	except ImportError as err:
		console.Exception('D2XP server 2nd import failed',err)
		console.Description('D2XP server error or not found')
state= 'd2xp' in servers
console.likeBoot('D2XP server',state)

def populateEnabled():
	
	global enabled,requirements,enable,parsers,servers
	ke=requirements.keys()
	for k in ke:
		thereq=True
		if k not in enable:
			thereq=False
		par, ser=requirements[k]
		for p in par:
			if p not in parsers.keys():
				thereq=False
		for s in ser:
			if s not in servers.keys():
				thereq=False
		if thereq:
			enabled.append(k)
	
class tcp(socketserver.BaseRequestHandler):
	"""
	The RequestHandler class for our server.

	It is instantiated once per connection to the server, and must
	override the handle() method to implement communication to the
	client.
	"""

	def handle(self):
	
		self.productID=''
		
		while self.productID is '':
			
			self.rcv_pack=self.request.recv(RCV_BUFFER_LENGTH)
			# self.request is the TCP socket connected to the client
			
			if debug:
				print(self.client_address[0],self.rcv_pack,sep='<-',end='\n')
			
			self.result=common.getHeadedMessage(self.rcv_pack)
			
			#TODO: check for handshake and initialization
			if self.result['packageTypeNumber'] == '0x50':
				self.result.update(bnc.battle_CS_50(self.result['packedMessage']))
				self.platformID=self.result['Platform ID'][::-1].lower().decode(encoding="utf-8")
				self.productID=self.result['Product ID'][::-1].lower().decode(encoding="utf-8")
			
			if verbose or debug:
				# print('<-received:',result['packageType'],end='\n')
				print(self.client_address[0],'received',self.result,sep=':',end='\n')
			
			# if (self.result['packageType'] is 'UNKNOWN') and (not quiet):
				# print('details follow:',self.result,self.rcv_pack,sep='\n',end='\n')
		
		if self.productID in enabled:
			console.Message('welcome',self.productID,'client',self.client_address[0],sep=' ')
			servers[self.productID].begin(self)
		else:
			console.Message('there is no service for',self.productID,'client',self.client_address[0],sep=' ')

def start():
	console.pieceOfLine('configured for ')
	console.Message(HOST,PORT,sep=':')
	
	# Create the server, binding to localhost on port 9999
	server = socketserver.TCPServer((HOST, PORT), tcp)
	
	console.Message('waiting for clients...')
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()

if __name__ == "__main__":
	
	# registerParsers()
	# registerServers()
	populateEnabled()
	start()

def dissectPackage(bytesPackage):

	packageInfo=getHeadedMessage(bytesPackage)
	if packageInfo['packageTypeNumber'] == '0x50':
		unpackedMessage=battle_CS_50(packageInfo['packedMessage'])
		unpackedMessage['Platform ID']=unpackedMessage['Platform ID'][::-1]
		unpackedMessage['Product ID']=unpackedMessage['Product ID'][::-1]
		# unpackedMessage['Local IP']=bytes(str(unpackedMessage['Local IP']),'utf-8')
		# print('bytes:',unpackedMessage['Local IP'],'\n')
		# unpackedMessage['Local IP']=unpackedMessage['Local IP'][::-1]
		# print('reversed bytes:',unpackedMessage['Local IP'],'\n')
		# unpackedMessage['Local IP']=utils.IntToDottedIP(int(unpackedMessage['Local IP']))
		packageInfo.update(unpackedMessage)
		return packageInfo
	
	# if packageType is 0:
		# packageInfo['packageType']='CLIENT_PINGREQ'
		# messageInfo=CLIENT_PINGREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 2:
		# packageInfo['packageType']='CLIENT_CLOSEGAME'
		# messageInfo=CLIENT_CLOSEGAME(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 37:
		# packageInfo['packageType']='CLIENT_ECHOREPLY'
		# messageInfo=CLIENT_ECHOREPLY(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 38:
		# packageInfo['packageType']='CLIENT_STATSREQ'
		# messageInfo=CLIENT_STATSREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 41:
		# packageInfo['packageType']='CLIENT_LOGINREQ1'
		# messageInfo=CLIENT_LOGINREQ1(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 45:
		# packageInfo['packageType']='CLIENT_ICONREQ'
		# messageInfo=CLIENT_ICONREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 49:
		# packageInfo['packageType']='CLIENT_CHANGEPASSREQ'
		# messageInfo=CLIENT_CHANGEPASSREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 51:
		# packageInfo['packageType']='CLIENT_FILEINFOREQ'
		# messageInfo=CLIENT_FILEINFOREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 61:
		# packageInfo['packageType']='CLIENT_CREATEACCTREQ2'
		# messageInfo=CLIENT_CREATEACCTREQ2(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 80:
		# packageInfo['packageType']='CLIENT_COUNTRYINFO_109'
		# messageInfo=CLIENT_COUNTRYINFO_109(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 81:
		# packageInfo['packageType']='CLIENT_AUTHREQ_109'
		# messageInfo=CLIENT_AUTHREQ_109(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 82:
		# packageInfo['packageType']='CLIENT_CREATEACCOUNT_W3'
		# messageInfo=CLIENT_CREATEACCOUNT_W3(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 83:
		# packageInfo['packageType']='CLIENT_LOGINREQ_W3'
		# messageInfo=CLIENT_LOGINREQ_W3(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 90:
		# packageInfo['packageType']='CLIENT_GETPASSWORDREQ'
		# messageInfo=CLIENT_GETPASSWORDREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
	# elif packageType is 91:
		# packageInfo['packageType']='CLIENT_CHANGEEMAILREQ'
		# messageInfo=CLIENT_CHANGEEMAILREQ(ActualPacket=bytesPackage,toMakeAPackage=False)
		# messageInfo.update(packageInfo)
		# return messageInfo
		
	else:
		packageInfo['packageType']='UNKNOWN'
		return packageInfo
