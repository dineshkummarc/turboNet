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
	