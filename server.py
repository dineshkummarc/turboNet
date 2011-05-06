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
debug=False

# game='war3'
game='starx'

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
				print('<-',rcv_pack,end='\n')
			
			result=bnet_protocol.dissectPackage(rcv_pack)
			if verbose or debug:
				print('<-received:',result['packageType'],end='\n')
			
			if result['packageType'] is 'UNKNOWN':
				print('details follow:',result,rcv_pack,sep='\n',end='\n')
			
			if result['packageType'] is 'pingPackage':
				if alreadyPing: break
				else:
					answer='ping...'
					clientsock.send(b'')
					alreadyPing=True
			else: 
				alreadyPing=False
				
				if game is 'war3':
					if result['packageType'] is 'initPackage':
						answer='helo!'
						clientsock.send(b'')	
					elif result['packageType'] is 'CLIENT_COUNTRYINFO_109':
						answer = bnet_protocol.SERVER_ECHOREQ()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_ECHOREPLY':
						# answer = bnet_protocol.SERVER_AUTHREQ_109(data={'length':229})
						f=open('SERVER_AUTHREQ_109.dump','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_AUTHREQ_109':
						# answer = bnet_protocol.SERVER_AUTHREPLY_109(data={'length':9})
						f=open('SERVER_AUTHREPLY_109.dump','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_FILEINFOREQ':
						# answer = bnet_protocol.SERVER_FILEINFOREPLY(data={'length':9})
						if not alrdy_tos:
							f=open('SERVER_FILEINFOREPLY-termsofservice-enUS.txt.dump','rb')
							answer=f.read()
							f.close()
							alrdy_tos=True
						elif not alrdy_nwacc:
							f=open('SERVER_FILEINFOREPLY-newaccount-enUS.txt.dump','rb')
							answer=f.read()
							f.close()
							alrdy_nwacc=True
						elif not alrdy_chthlp:
							f=open('SERVER_FILEINFOREPLY-chathelp-war3-enUS.txt.dump','rb')
							answer=f.read()
							f.close()
							alrdy_chthlp=True
						elif not alrdy_bnsvr:
							f=open('SERVER_FILEINFOREPLY-bnserver-WAR3.ini.dump','rb')
							answer=f.read()
							f.close()
							alrdy_bnsvr=True	
						else: answer=b'not-yet'
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_ICONREQ':
						# answer = bnet_protocol.SERVER_ICONREPLY()
						f=open('SERVER_ICONREPLY.dump','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					else:
						answer='NOW WHAT!!!???'
						
				elif game is 'starx':
					if result['packageType'] is 'initPackage':
						answer='helo!'
						clientsock.send(b'')	
					elif result['packageType'] is 'CLIENT_COUNTRYINFO_109':
						answer = bnet_protocol.SERVER_ECHOREQ()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_ECHOREPLY':
						# answer = bnet_protocol.SERVER_AUTHREQ_109(data={'length':229})
						f=open('SERVER_AUTHREQ_109.star','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_AUTHREQ_109':
						# answer = bnet_protocol.SERVER_AUTHREPLY_109(data={'length':9})
						f=open('SERVER_AUTHREPLY_109.star','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_FILEINFOREQ':
						# answer = bnet_protocol.SERVER_FILEINFOREPLY(data={'length':9})
						if not alrdy_tos:
							f=open('SERVER_FILEINFOREPLY-icons_star.bni.star','rb')
							answer=f.read()
							f.close()
							alrdy_tos=True
						elif not alrdy_nwacc:
							f=open('SERVER_FILEINFOREPLY-tos_USA.txt.star','rb')
							answer=f.read()
							f.close()
							alrdy_nwacc=True
						elif not alrdy_chthlp:
							f=open('SERVER_FILEINFOREPLY-bnserver.ini.star','rb')
							answer=f.read()
							f.close()
							alrdy_chthlp=True
						else: answer=b'not-yet'
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_ICONREQ':
						# answer = bnet_protocol.SERVER_ICONREPLY()
						f=open('SERVER_ICONREPLY.star','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					elif result['packageType'] is 'CLIENT_STATSREQ':
						# answer = bnet_protocol.SERVER_STATSREPLY()
						f=open('SERVER_STATSREPLY.star','rb')
						answer=f.read()
						f.close()
						clientsock.send(answer)
					
					elif result['packageType'] is 'CLIENT_CLOSEGAME':
						answer = 'finished!'
						clientsock.close()
					else:
						answer='NOW WHAT!!!???'
					
			if debug:
				print('->',answer,end='\n')
		
	except socket.error:
		print('socket error\n')
	
	clientsock.close()
	print('...disconnected from:',addr,end='\n')
	retransferFiles()

serversock.close()
time.sleep(12000)
