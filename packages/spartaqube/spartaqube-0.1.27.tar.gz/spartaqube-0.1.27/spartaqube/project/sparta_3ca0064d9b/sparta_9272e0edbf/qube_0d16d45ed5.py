import os
from project.sparta_3ca0064d9b.sparta_9272e0edbf.qube_234d350ba7 import qube_234d350ba7
from project.sparta_3ca0064d9b.sparta_9272e0edbf.qube_9492ef67ec import qube_9492ef67ec
from project.sparta_3ca0064d9b.sparta_9272e0edbf.qube_229d13dbf1 import qube_229d13dbf1
from project.sparta_3ca0064d9b.sparta_9272e0edbf.qube_28a3c2677a import qube_28a3c2677a
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_234d350ba7()
		elif A.dbType==1:A.dbCon=qube_9492ef67ec()
		elif A.dbType==2:A.dbCon=qube_229d13dbf1()
		elif A.dbType==4:A.dbCon=qube_28a3c2677a()
		return A.dbCon