from project.sparta_c8e521c5f3.sparta_2d3afe987d.qube_c1f8f8d54e import EngineBuilder
class PostgresConnector(EngineBuilder):
	def __init__(A,host,port,user,password,database):super().__init__(host=host,port=port,user=user,password=password,database=database,engine_name='postgresql');A.connector=A.build_postgres()
	def test_connection(A):
		B=False
		try:
			if A.connector:A.connector.close();return True
			else:return B
		except Exception as C:print(f"Error: {C}");return B