import time
def sparta_389aec9a4f():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_389aec9a4f()
def sparta_080e0c148c(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_631870a13b():sparta_080e0c148c(False)