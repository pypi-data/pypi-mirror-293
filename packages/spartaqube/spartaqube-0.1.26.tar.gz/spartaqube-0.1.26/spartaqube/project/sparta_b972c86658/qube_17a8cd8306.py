import time
def sparta_d1ec1b1c6d():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_d1ec1b1c6d()
def sparta_ca3608dd89(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_fd7ac09868():sparta_ca3608dd89(False)