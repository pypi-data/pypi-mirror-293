import time
def sparta_8665ab42c1():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_8665ab42c1()
def sparta_5e16c5ce61(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_093a46fa13():sparta_5e16c5ce61(False)