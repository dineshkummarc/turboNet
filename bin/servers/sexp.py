
def begin(handler):
	print('entering the Starcraft Broodwar server')
	ans=True
	while ans:
		ans=handler.request.recv(1024)

