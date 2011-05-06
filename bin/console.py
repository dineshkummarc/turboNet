
debug=False
verbose=False
quiet=False

def Debug(theString):
	if debug:
		print(theString)

def Exception(thestr,err):
	if debug:
		print(thestr,err,sep='->',end='\n')
		
def Description(theString):
	if verbose:
		print(theString)

def Message(*theString,sep=''):
	if not quiet:
		print(*theString,sep=sep)

def pieceOfLine(theString):
	if not quiet:
		print(theString,end='')
		
def likeBoot(element,state=False):
	if not quiet:
		if state:
			tateStr="load"
		else:
			tateStr="fail"
		print(element,'\t',end='')
		print('[',tateStr,']',sep='',end='\n')