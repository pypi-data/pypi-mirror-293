import time
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.qube_65b2e05bb0 import EngineBuilder
class MariadbConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='mysql');A.connector=A.build_mariadb()
	def test_connection(A):
		B=False
		try:
			if A.connector.is_connected():A.connector.close();return True
			else:return B
		except Exception as C:print(f"Error: {C}");return B