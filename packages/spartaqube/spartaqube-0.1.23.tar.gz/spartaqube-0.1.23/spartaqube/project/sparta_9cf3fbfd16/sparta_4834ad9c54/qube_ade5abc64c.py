import os
from project.sparta_9cf3fbfd16.sparta_4834ad9c54.qube_8f9affdb9c import qube_8f9affdb9c
from project.sparta_9cf3fbfd16.sparta_4834ad9c54.qube_84df7fc8ce import qube_84df7fc8ce
from project.sparta_9cf3fbfd16.sparta_4834ad9c54.qube_4ee6cfaa07 import qube_4ee6cfaa07
from project.sparta_9cf3fbfd16.sparta_4834ad9c54.qube_05697c0fe3 import qube_05697c0fe3
class db_connection:
	def __init__(A,dbType=0):A.dbType=dbType;A.dbCon=None
	def get_db_type(A):return A.dbType
	def getConnection(A):
		if A.dbType==0:
			from django.conf import settings as B
			if B.PLATFORM in['SANDBOX','SANDBOX_MYSQL']:return
			A.dbCon=qube_8f9affdb9c()
		elif A.dbType==1:A.dbCon=qube_84df7fc8ce()
		elif A.dbType==2:A.dbCon=qube_4ee6cfaa07()
		elif A.dbType==4:A.dbCon=qube_05697c0fe3()
		return A.dbCon