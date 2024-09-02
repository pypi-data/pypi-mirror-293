import os
from project.sparta_d7b94e3744.sparta_dafc7c5b86.qube_cefd16cb03 import qube_cefd16cb03
from project.sparta_d7b94e3744.sparta_dafc7c5b86.qube_080875829a import qube_080875829a
from project.sparta_d7b94e3744.sparta_dafc7c5b86.qube_1be1238a32 import qube_1be1238a32
from project.sparta_d7b94e3744.sparta_dafc7c5b86.qube_935db0b40f import qube_935db0b40f
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_cefd16cb03()
		elif A.dbType==1:A.dbCon=qube_080875829a()
		elif A.dbType==2:A.dbCon=qube_1be1238a32()
		elif A.dbType==4:A.dbCon=qube_935db0b40f()
		return A.dbCon