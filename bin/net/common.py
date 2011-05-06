import struct

debug=False

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
			
			actualPackageLength=len(ActualPackage)
			
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
							'actualPackageLength':actualPackageLength,
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
	
	if debug:
		print('unpacking: ',packedData,end='\n')
		print('with format: ',format,end='\n')
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
