import socket
import time
import bnet_protocol

HOST = '127.0.0.1'
PORT = 6112
ADDR = (HOST, PORT)
RCV_BUFFER_LENGTH = 2048
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(ADDR)
serversock.listen(1)

verbose=False
debug=True

# game='war3'
# game='starx'

def retransferFiles():
	global alrdy_tos,alrdy_nwacc,alrdy_chthlp,alrdy_bnsvr
	alrdy_tos=False
	alrdy_nwacc=False
	alrdy_chthlp=False
	alrdy_bnsvr=False

retransferFiles()
	
while 1:
	print('waiting...',end='\n')
	
	clientsock, addr = serversock.accept()
	print('connected:',addr,end='\n')
	
	alreadyPing=False
	try:
		while 1:
		
			rcv_pack=clientsock.recv(RCV_BUFFER_LENGTH)
			if debug:
				print('incoming package',rcv_pack,sep='<-',end='\n')
			
			result=bnet_protocol.dissectPackage(rcv_pack)
			if verbose or debug:
				# print('<-received:',result['packageType'],end='\n')
				print('received',result,sep=':',end='\n')
			
			# if result['packageType'] is 'UNKNOWN':
				# print('details follow:',result,rcv_pack,sep='\n',end='\n')
			
			md={'Logon Type':0,
				'Server Token':259,
				'UDPValue':1027,
				'MPQ filetime':10261026,
				'IX86ver filename':'jejejejeje.mpq',
				}
			# answer=bnet_protocol.packMessage_2(modelForm=bnet_protocol.battle_SC_50(md),unpackedData=md)
			
			# if debug:
				# print('->',answer,end='\n')
		
	except socket.error:
		print('socket error\n')
	
	clientsock.close()
	print('...disconnected from:',addr,end='\n')
	retransferFiles()

serversock.close()
time.sleep(12000)
