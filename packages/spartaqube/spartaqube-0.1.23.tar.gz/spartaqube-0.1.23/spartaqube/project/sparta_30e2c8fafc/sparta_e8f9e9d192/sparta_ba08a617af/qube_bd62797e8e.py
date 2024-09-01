_A=None
import redis,pandas as pd
from project.sparta_30e2c8fafc.sparta_e8f9e9d192.qube_175ee3321a import EngineBuilder
from project.sparta_30e2c8fafc.sparta_e8608fa6bc.qube_e278700345 import sparta_389be66ef5
class RedisConnector(EngineBuilder):
	def __init__(A,host,port,user=_A,password=_A,db=0):super().__init__(host=host,port=port,user=user,password=password,engine_name='redis');A.connector=A.build_redis(db=db)
	def test_connection(A):
		B=False
		try:
			if A.connector.ping():return True
			else:return B
		except Exception as C:A.error_msg_test_connection=str(C);return B
	def get_keys(A):B=A.connector.keys('*');return[A.decode()for A in B]
	def get(B,key):
		C=key;D=B.connector.type(C).decode()
		if D=='string':
			F=B.connector.get(C)
			if F is not _A:return F.decode()
		elif D=='list':
			A=B.connector.lrange(C,0,-1)
			if A is not _A:A=[A.decode()for A in A];return A
		elif D=='hash':
			A=B.connector.hgetall(C)
			if A is not _A:A=[A.decode()for A in A];return A
		elif D=='set':
			E=B.connector.smembers(C)
			if E is not _A:E=[A.decode()for A in E];return E
		elif D=='zset':
			A=B.connector.zrange(C,0,-1,withscores=True)
			if A is not _A:A=[A.decode()for A in A]
		else:return
	def get_available_tables(A):
		try:return sorted(A.get_keys())
		except Exception as B:print('get available tables error');print(B)
		return[]
	def get_table_columns(A,table_name):return[table_name]
	def get_data_table(C,table_name):A=table_name;D=C.get(A);B=sparta_389be66ef5(D);B.columns=[A];return B