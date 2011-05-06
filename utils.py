
#from http://snipplr.com/view/14807/convert-ip-to-int-and-int-to-ip/
def IntToDottedIP( intip ):
	octet = ''
	for exp in [3,2,1,0]:
		octet = octet + str(intip / ( 256 ** exp )) + "-"
		intip = intip % ( 256 ** exp )
	return(octet.rstrip('.'))