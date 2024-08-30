import time
def sparta_bccafbb8f2():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_bccafbb8f2()
def sparta_9c4e9070f7(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_a005023120():sparta_9c4e9070f7(False)