import os
from project.sparta_b972c86658.sparta_ddb5763411.qube_c6aed8f50b import qube_c6aed8f50b
from project.sparta_b972c86658.sparta_ddb5763411.qube_61d75ee8bb import qube_61d75ee8bb
from project.sparta_b972c86658.sparta_ddb5763411.qube_c713b348da import qube_c713b348da
from project.sparta_b972c86658.sparta_ddb5763411.qube_6366743fb5 import qube_6366743fb5
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_c6aed8f50b()
		elif A.dbType==1:A.dbCon=qube_61d75ee8bb()
		elif A.dbType==2:A.dbCon=qube_c713b348da()
		elif A.dbType==4:A.dbCon=qube_6366743fb5()
		return A.dbCon