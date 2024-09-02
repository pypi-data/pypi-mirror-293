import time
def sparta_5edd89f3d0():
	B=0;A=time.time()
	while True:B=A;A=time.time();yield A-B
TicToc=sparta_5edd89f3d0()
def sparta_dbaf9807ad(tempBool=True):
	A=next(TicToc)
	if tempBool:print('Elapsed time: %f seconds.\n'%A);return A
def sparta_bfbe41862e():sparta_dbaf9807ad(False)