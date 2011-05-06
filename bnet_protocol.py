import struct
import time
import random
import utils

'''Battle.net protocol format strings
	Strings formatting and documentation for battle.net packages
'''

def getHeadedMessage(ActualPackage):
	
	if not ActualPackage:
		packageInfo ={	'packageHeader':None,
						'packageTypeNumber':'0x00',
						'packageLength':0,
						'packedMessage':None,
					}
	else:
		if len(ActualPackage) is 1:	
			packageHeadArea = struct.unpack('!B',ActualPackage)
			packageInfo ={	'packageHeader':hex(packageHeadArea[0]),
							'packageTypeNumber':'0x00',
							'packageLength':1,
							'packedMessage':None,
						}
		else:
			packageStartByte = struct.unpack('!B'+str(len(ActualPackage)-1)+'s',ActualPackage)
			
			if packageStartByte[0] is 1:
				print('FIXME: starting bit in a package with payload')
				packageHeadArea = struct.unpack('!BBBH'+str(len(ActualPackage)-5)+'s',ActualPackage)
				packageStart, packageHeader, packageTypeNumber, packageLength, packedMessage =packageHeadArea
			else:
				packageHeadArea = struct.unpack('!BBH'+str(len(ActualPackage)-4)+'s',ActualPackage)
				packageHeader, packageTypeNumber, packageLength, packedMessage =packageHeadArea
			
			packageInfo = {	'packageHeader':packageHeader,
							'packageTypeNumber':hex(packageTypeNumber),
							'packageLength':packageLength,
							'packedMessage':packedMessage,
							}
	
	return packageInfo
	

def packMessage(pck):
	
	format='!'
	values=[]
	# print('prepare for packing: ',pck,end='\n')
	for fmt_itm,value in pck:
		format+=fmt_itm
		valuestr=str(value)
		fmt_itmstr=str(fmt_itm)
		if not valuestr.isdigit():
			valuebts=bytearray(valuestr,'ascii')
			value=list(valuebts)
			values.extend(value)
		elif not fmt_itmstr.isalpha():
			count=int(fmt_itmstr[:-1])
			lotofvalues=[]
			for some in range(0,count):
				lotofvalues.append(value)
			values.extend(lotofvalues)
		else:
			values.append(value)
	values=tuple(values)
	# print('format',format,end='\n')
	# print('values',values,end='\n')
	return struct.pack(format,*values)

def unpackMessage(model,actual):
	
	format='!'
	
	for fmt_itm,value in model:
		format+=fmt_itm
	# print('unpacking: ',actual,end='\n')
	# print('with format: ',format,end='\n')
	return struct.unpack(format,actual)

def unpackMessage_2(modelForm,packedData):
	
	format=''
	names=[]
	
	for fmt_itm,name,validValues in modelForm:
		format+=fmt_itm
		names.append(name)
	
	# print('unpacking: ',packedData,end='\n')
	# print('with format: ',format,end='\n')
	# print('need (bytes): ',struct.calcsize(format),end='\n')
	# print('have (bytes): ',len(packedData),end='\n')
	
	unpackedData=struct.unpack(format,packedData)
	
	packedItemIterator=0
	messageInfo={}
	
	for fmt_itm,name,validValues in modelForm:
		if fmt_itm[-1] != 'c':
			messageInfo[name]=unpackedData[packedItemIterator]
			packedItemIterator+=1
		else:
			sumData=''
			for noMatter in range(int(fmt_itm[:-1])):
				sumData+=unpackedData[packedItemIterator]
				packedItemIterator+=1
			messageInfo[name]=sumData

	return messageInfo

def packMessage_2(modelForm,unpackedData):
	
	format='!'
	values=[]
	# print('prepare for packing: ',pck,end='\n')
	for fmt_itm,value in pck:
		format+=fmt_itm
		valuestr=str(value)
		fmt_itmstr=str(fmt_itm)
		if not valuestr.isdigit():
			valuebts=bytearray(valuestr,'ascii')
			value=list(valuebts)
			values.extend(value)
		elif not fmt_itmstr.isalpha():
			count=int(fmt_itmstr[:-1])
			lotofvalues=[]
			for some in range(0,count):
				lotofvalues.append(value)
			values.extend(lotofvalues)
		else:
			values.append(value)
	values=tuple(values)
	# print('format',format,end='\n')
	# print('values',values,end='\n')
	return struct.pack(format,*values)

def battle_CS_00():
	pass

def battle_CS_02():
	pass

def battle_CS_50(packedMessage):
	
	# print('tamaño',len(packedMessage),sep=':',end='\n')
	
	pck_format=[('I','Protocol ID',[0]),
				('4s','Platform ID',['IX86','PMAC','XMAC']),
				('4s','Product ID',[]),
				('I','Version Byte',[]),
				('4s','Product language',[0]),
				('I','Local IP',[]),	# for NAT compatibility
				('I','Time zone bias',[0]),
				('I','Locale ID',[]),
				('I','Language ID',[]),
				(str(len(packedMessage)-36)+'s','Country abreviation and Country',[]),
				]
	unpackedMessage=unpackMessage_2(modelForm=pck_format,packedData=packedMessage)
	return unpackedMessage

def battle_SC_50(messageData):
	
	pck_format=[('I','Logon Type',['0x00','0x01','0x02']),
				('I','Server Token',[]),
				('I','UDPValue',[]),
				('Q','MPQ filetime',[]),
				(str(len(packedMessage)-20)+'B','IX86ver filename',[]),
				# ('-1s','ValueString',[]),
				]
	
	return pck_format
	
	
	
def CLIENT_INIT(packet=False,pack=True):

	pck_static_size=19
	pck=[('B',1),		#unknown
		]
	if(pack):	
		pass	#TODO -> client package
	else:
		unpck=unpackMessage(model=pck,actual=packet)
		return {'unknown':unpck[0],
				}

def CLIENT_PINGREQ(ActualPacket=False,toMakeAPackage=True):

	pck_static_size=4
	pck=[('B',255),	#unknown
		('B',0),	#type
		('B',4),	#size
		('B',0),	#Os (0)
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'Os':unpck[3],
				}

def CLIENT_CLOSEGAME(ActualPacket=False,toMakeAPackage=True):

	pck_static_size=4
	pck=[('B',255),	#unknown
		('B',2),	#type
		('B',4),	#size
		('B',0),	#Os (0)
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'Os':unpck[3],
				}
				
def CLIENT_ECHOREPLY(ActualPacket=False,toMakeAPackage=True):

	pck_static_size=8
	pck=[('B',255),	#unknown
		('B',37),	#type
		('B',0),	#size
		('B',0),	#padding
		('I',0),	#ticks
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'ticks':unpck[4],
				}

def CLIENT_STATSREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=15
	pck=[('B',255),		#unknown
		('B',38),		#type
		('B',0),		#size
		('I',0),		#name_count;
		('I',0),		#key_count;
		('I',0),		#requestid; /* 78 52 82 02 */
		('-1s',0),		# /* player name */
    # /* field key ... */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[6]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'empty':unpck[3],
				}

def CLIENT_LOGINREQ1(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=31
	pck=[('B',255),		#unknown
		('B',38),		#type
		('B',0),		#size
		('I',0),		#ticks;
		('I',0),		#sessionkey;
		('I',0),		#password_hash2[5]; /* hash of ticks, key, and hash1 */
		('I',0),
		('I',0),
		('I',0),
		('I',0),
		('-1s',0),		#/* player name */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[10]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'ticks':unpck[3],
				'ticks':unpck[4],
				'ticks':(unpck[5],unpck[6],unpck[7],unpck[8],unpck[9]),
				'ticks':unpck[10],
				}

def CLIENT_ICONREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=4
	pck=[('B',255),		#unknown
		('B',45),		#type
		('B',0),		#size
		('B',0),		#empty?
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'empty':unpck[3],
				}

def CLIENT_CHANGEPASSREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=51
	pck=[('B',255),		#unknown
		('B',49),		#type
		('B',0),		#size
		('I',0),		#ticks; /* FIXME: upper two bytes seem constant for each client? */
		('I',0),		#sessionkey;
		('I',0),		#oldpassword_hash2[5]; /* hash of ticks, key, hash1 */
		('I',0),
		('I',0),
		('I',0),
		('I',0),
		('I',0),		#newpassword_hash1[5]; /* hash of lowercase password w/o null */
		('I',0),
		('I',0),
		('I',0),
		('I',0),
		('-1s',0),		#/* player name */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[15]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'ticks':unpck[3],
				'sessionkey':unpck[4],
				'oldpassword_hash2':(unpck[5],unpck[6],unpck[7],unpck[8],unpck[9]),
				'newpassword_hash1':(unpck[10],unpck[11],unpck[12],unpck[13],unpck[14]),
				'player_name':unpck[15],
				}
				
def CLIENT_FILEINFOREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=11
	pck=[('B',255),		#unknown
		('B',51),		#type
		('B',0),		#size
		('I',0),		#type;     /* type of file (TOS,icons,etc.) */
		('I',0),		#unknown2; /* 00 00 00 00 */ /* always zero? */
		('-1s',0),		# /* filename */          /* default/suggested filename? */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[5]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'Ttype':unpck[3],
				'unknown2':unpck[4],
				'filename':unpck[5],
				}

def CLIENT_CREATEACCTREQ2(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=23
	pck=[('B',255),		#unknown
		('B',61),		#type
		('B',0),		#size
		('I',0),		#password_hash1[5];
		('I',0),
		('I',0),
		('I',0),
		('I',0),
		('-1s',0),		# /* username (charactername?) */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[8]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'password_hash1':(unpck[3],unpck[4],unpck[5],unpck[6],unpck[7]),
				'username':unpck[8],
				}


def CLIENT_COUNTRYINFO_109(ActualPacket=False,toMakeAPackage=True):

	pck_static_size=44
	pck=[('B',255),		#unknown
		('B',80),		#type
		('B',0),		#size
		('I',0),		#protocol /* 00 00 00 00 always zero */
		('I',0),		#archtag
		('I',0),		#clienttag
		('I',0),		#versionid /* 09 00 00 00 */ /* FIXME: what is this? */
		('I',0),		#gamelang
		('I',0),		#localip
		('I',0),		#bias
		('I',0),		#lcid
		('I',0),		#langid
		('s',0),
		('3s',0),		#langstr
		('s',0),
		('-1s',0),		#countryname
		('s',0),
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[15]=(str(len(ActualPacket)-pck_static_size-1)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'protocol':unpck[3],
				'archtag':unpck[4],
				'clienttag':unpck[5],
				'versionid':unpck[6],
				'gamelag':unpck[7],
				'localip':unpck[8],
				'bias':unpck[9],
				'lcid':unpck[10],
				'langid':unpck[11],
				'langstr':unpck[13],
				'countryname':unpck[15],
				}

def CLIENT_AUTHREQ_109(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=23
	pck=[('B',255),		#unknown
		('B',81),		#type
		('B',0),		#size
		('I',0),		#ticks
		('I',0),		#gameversion
		('I',0),		#checksum
		('I',0),		#cdkey_number; /* count of cdkeys, d2 = 1, lod = 2 */
		('I',0),		#spawn; 	/* set if using spawn copy */
		('-1s',0),		# /* cdkey info(s) */
						# /* executable info */
						# /* cdkey owner */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[8]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'ticks':unpck[3],
				'gameversion':unpck[4],
				'checksum':unpck[5],
				'cdkey_number':unpck[6],
				'spawn':unpck[7],
				'else':unpck[8],
				}

def CLIENT_CREATEACCOUNT_W3(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=67
	pck=[('B',255),		#unknown
		('B',82),		#type
		('B',0),		#size
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('-1s',0)		#/* player name */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[67]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'player':unpck[67],
				'unk_all':unpck,
				}

def CLIENT_LOGINREQ_W3(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=35
	pck=[('B',255),		#unknown
		('B',83),		#type
		('B',0),		#size
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('B',0),		#trash
		('-1s',0)		#/* player name */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[35]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'player':unpck[35],
				'unk_all':unpck,
				}

def CLIENT_GETPASSWORDREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=3
	pck=[('B',255),		#unknown
		('B',91),		#type
		('B',0),		#size
		('-1s',0),		#/* account name */
	# /* email address */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[3]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'everything':unpck[3],
				}


def CLIENT_CHANGEEMAILREQ(ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=3
	pck=[('B',255),		#unknown
		('B',91),		#type
		('B',0),		#size
		('-1s',0),		#/* account name */
	# /* old email address */
	# /* new email address */
		]
	if(toMakeAPackage):	
		pass	#TODO -> client package
	else:
		pck[3]=(str(len(ActualPacket)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=ActualPacket)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'everything':unpck[3],
				}

				
def CLIENT_COMPINFO1(packet=False,pack=True):

	pck_static_size=19
	pck=[('B',255),		#unknown
		('B',-1),		#type
		('B',0),		#size
		('I',0),		#reg_version;  /* 01 00 00 00 */
		('I',0),		#reg_auth;     /* D1 43 88 AA */ /* looks like server ip */
		('I',0),		#client_id;    /* DA 9D 1B 00 */
		('I',0),		#client_token; /* 9A F7 69 AB */
		]
	if(pack):	
		pass	#TODO -> client package
	else:
		pck[9]=(str(len(packet)-pck_static_size)+'s',0)
		return unpackMessage(model=pck,actual=packet)
		
def CLIENT_COUNTRYINFO1(packet=False,pack=True):

	pck_static_size=35
	pck=[('B',255),	#unknown
		('B',-1),	#type
		('B',0),	#size
		('Q',0),	#GMT
		('Q',0),	#local time
		('i',0),	#(gmt-local)/60  (using signed math)
		('I',0),	#09 04 00 00		12 04 00 00
		('I',0),	#09 04 00 00		12 04 00 00
		('I',0),	#09 04 00 00		12 04 00 00
		('s',0),	#more...
		]
	if(pack):	
		pass	#TODO -> client package
	else:
		pck[9]=(str(len(packet)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=packet)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'GMT':unpck[3],
				'local time':unpck[4],
				'bias':unpck[5],
				'unk1':unpck[6],
				'unk2':unpck[7],
				'unk3':unpck[8],
				'more':unpck[9],
				}

def CLIENT_AUTHREQ1(packet=False,pack=True):
	
	pck_static_size=23
	pck=[('B',255),		#unknown
		('B',-1),		#type
		('B',0),		#size
		('I',0),		#archtag
		('I',0),		#clienttag
		('I',0),		#versionid
		('I',0),		#gameversion
		('I',0),		#checksum
		('s',0),		#/* executable info */
		]
	if(pack):	
		pass	#TODO -> client package
	else:
		pck[8]=(str(len(packet)-pck_static_size)+'s',0)
		unpck=unpackMessage(model=pck,actual=packet)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'archtag':unpck[3],
				'clienttag':unpck[4],
				'versionid':unpck[5],
				'gameversion':unpck[6],
				'checksum':unpck[7],
				'exeinfo':unpck[8],
				}


def SERVER_PINGREPLY(data={'sequence':random.getrandbits(32)},packet=False,pack=True):

	pck_static_size=4
	pck=[('B',255),				#unknown
		('B',0),				#type
		('B',4),				#size
		('B',0),				#Os (0)
		]
	if(pack):	
		return packMessage(pck)
	else:
		unpck=unpackMessage(model=pck,actual=packet)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'Os':unpck[3],
				}
			
def SERVER_ECHOREQ(data={'sequence':random.getrandbits(32)},packet=False,pack=True):

	pck_static_size=8
	pck=[('B',255),				#unknown
		('B',37),				#type
		('B',8),				#size
		('B',0),				#padding
		('I',data['sequence']),	#ticks
		]
	if(pack):	
		return packMessage(pck)
	else:
		unpck=unpackMessage(model=pck,actual=packet)
		return {'unknown':unpck[0],
				'type':unpck[1],
				'size':unpck[2],
				'ticks':unpck[4],
				}

def SERVER_ICONREPLY(data=False,ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=11
	
	pck=[('B',255),	#unknown
		('B',51),	#type
		('B',0),	#size
		('Q',0),	#timestamp; /* file modification time? */
		('-1B',0),	#/* filename */
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package
		
def SERVER_STATSREPLY(data=False,ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=11
	
	pck=[('B',255),	#unknown
		('B',45),	#type
		('B',0),	#size
		('I',0),	#name_count;
		('I',0),	#key_count;
		('I',0),	#requestid; /* 78 52 82 02 */ /* EE E4 84 03 */ /* same as request */
		('-1B',0),	#/* field values ... */
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package

def SERVER_CHANGEPASSACK(data=False,ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=7
	
	pck=[('B',255),	#unknown
		('B',49),	#type
		('B',0),	#size
		('I',0),	#message;
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package

def SERVER_FILEINFOREPLY(data=False,ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=7
	
	pck=[('B',255),	#unknown
		('B',51),	#type
		('B',0),	#size
		('I',0),	#type;      /* type of file (TOS,icons,etc.) */
		('I',0),	#unknown2;  /* 00 00 00 00 */ /* same as in TOSREQ */
		('Q',0),	#timestamp; /* file modification time */
		('B',0),	#/* filename */
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package
		
def SERVER_MOTD_W3(news_body='',packet=False,pack=True):

	pck_static_size=22
	pck=[('B',255),								#unknown
		('B',70),								#type
		('B', pck_static_size+len(news_body)),	#size
		('B',0),								#message type; we only saw "1" type so far
		('I',int(time.time())),					#current server time
		('I',int(time.time())),					#oldest news timestamp
		('I',int(time.time())),					#this news item timestamp; it is equal with the latest news item timestamp for the welcome message
		('I',int(time.time())),					#redundant timestamp; always equal with the timestamp except the last packet which shows in the right panel
		('B',0),								#padding
		(str(len(news_body))+'s',bytearray(news_body,'utf-8')),	#news body
		('B',0),								#padding
		]
	if(pack):
		return packMessage(pck)
	else:
		pass #TODO -> server package

def SERVER_AUTHREQ_109(data=False,ActualPacket=False,toMakeAPackage=True):
	
	
	only_filename_so_far='IX86ver1.mpq'
	data['file']=only_filename_so_far
	
	only_equation_so_far='A=3845581634 B=880823580 C=1363937103 4 A=A-S B=B-C C=C-A A=A-B'
	data['equation']=only_equation_so_far
	
	pck_static_size=24
	filename_size=len(data['file'])
	equation_size=len(data['equation'])
	blank_space_size=data['length']-pck_static_size-filename_size-equation_size
	
	pck=[('B',255),									#unknown
		('B',80),									#type
		('B',0),									#size
		('I',0),									#logontype;  /* 00 00 00 00 always zero */
		('I',2),									#sessionkey;
		('I',0),									#sessionnum;
		('Q',int(time.time())),						#timestamp;
		('B',1),									#versioncheck
		(str(filename_size)+'B',data['file']),		#filename
		(str(equation_size)+'B',data['equation']),	#equation */
		(str(blank_space_size)+'B',0),				#blank space
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package

def SERVER_AUTHREPLY_109(data=False,ActualPacket=False,toMakeAPackage=True):
	
	pck_static_size=7
	
	pck=[('B',255),	#unknown
		('B',81),	#type
		('B',0),	#size
		('I',0),	#logontype;  /* 00 00 00 00 always zero */
		(str(data['length']-pck_static_size)+'B',0),	#/* message string? */
		]
	if(toMakeAPackage):
		return packMessage(pck)
	else:
		pass #TODO -> server package


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
		