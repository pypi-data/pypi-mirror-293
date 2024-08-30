import os
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_8fb7b29af3 import qube_8fb7b29af3
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_c2bd03b60f import qube_c2bd03b60f
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_28f0474d93 import qube_28f0474d93
from project.sparta_509f9a5b62.sparta_b9bfdd4f44.qube_99b41b2c7d import qube_99b41b2c7d
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_8fb7b29af3()
		elif A.dbType==1:A.dbCon=qube_c2bd03b60f()
		elif A.dbType==2:A.dbCon=qube_28f0474d93()
		elif A.dbType==4:A.dbCon=qube_99b41b2c7d()
		return A.dbCon