_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_40ba2b27bc.sparta_3a19c63ec4.qube_11d3c65eb8 as qube_11d3c65eb8
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_0b223451d3.qube_d2ffda5893 import ArcticConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_f575d060d9.qube_a4fe16ca6d import AerospikeConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_7b04c836a7.qube_e768380c6b import CassandraConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_3fa293d379.qube_cae28036e7 import ClickhouseConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_2d23b724ed.qube_98589906df import CouchdbConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_5b6e245092.qube_6610ee7504 import CsvConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_b9f38444c2.qube_7fec4224d2 import DuckDBConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_fc222f7d60.qube_d38bf79813 import JsonApiConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_1cdc55ef40.qube_6ff7dad2f6 import InfluxdbConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_8bcfe43d03.qube_214257329c import MariadbConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_8dae96a90a.qube_26dc6c33a1 import MongoConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_1cafd0b4a3.qube_f327a049d8 import MssqlConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_2c0354d696.qube_13fac9be45 import MysqlConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_ca4bfeb294.qube_bb0d367855 import OracleConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_ed7e438191.qube_59b5e0516c import ParquetConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_3bb2e1cce2.qube_83244eb73f import PostgresConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_19b1feaf26.qube_dc2b2945ca import PythonConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_e037457a5f.qube_634f592f5b import QuestDBConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_5af7ebaeac.qube_2e9bb56f7a import RedisConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_ac066e2bfb.qube_71d1fc7225 import ScylladbConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_8d1a80ef15.qube_584db46fa2 import SqliteConnector
from project.sparta_40ba2b27bc.sparta_3a19c63ec4.sparta_b619cca41f.qube_3a140a06ab import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_11d3c65eb8.sparta_f34bb1709b(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host;print('self.db_engine > '+str(A.db_engine))
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='arctic':A.db_connector=ArcticConnector(database_path=G,library_arctic=library_arctic)
		if A.db_engine=='cassandra':A.db_connector=CassandraConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='clickhouse':A.db_connector=ClickhouseConnector(host=B,port=C,database=F,user=D,password=E)
		if A.db_engine=='couchdb':A.db_connector=CouchdbConnector(host=B,port=C,user=D,password=E)
		if A.db_engine=='csv':A.db_connector=CsvConnector(csv_path=csv_path,csv_delimiter=csv_delimiter)
		if A.db_engine=='duckdb':A.db_connector=DuckDBConnector(database_path=G,read_only=read_only)
		if A.db_engine=='influxdb':A.db_connector=InfluxdbConnector(host=B,port=C,token=token,organization=organization,bucket=F,user=D,password=E)
		if A.db_engine==_C:A.db_connector=JsonApiConnector(json_url=json_url,dynamic_inputs=H,py_code_processing=I)
		if A.db_engine=='mariadb':A.db_connector=MariadbConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mongo':A.db_connector=MongoConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='mssql':A.db_connector=MssqlConnector(host=B,port=C,trusted_connection=trusted_connection,driver=driver,user=D,password=E,database=F)
		if A.db_engine=='mysql':A.db_connector=MysqlConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='oracle':A.db_connector=OracleConnector(host=B,port=C,user=D,password=E,database=F,lib_dir=lib_dir,oracle_service_name=oracle_service_name)
		if A.db_engine=='parquet':A.db_connector=ParquetConnector(database_path=G)
		if A.db_engine==_B:A.db_connector=PostgresConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='python':A.db_connector=PythonConnector(py_code_processing=I,dynamic_inputs=H)
		if A.db_engine=='questdb':A.db_connector=QuestDBConnector(host=B,port=C,user=D,password=E,database=F)
		if A.db_engine=='redis':A.db_connector=RedisConnector(host=B,port=C,user=D,password=E,db=redis_db)
		if A.db_engine=='scylladb':A.db_connector=ScylladbConnector(host=B,port=C,user=D,password=E,keyspace=J)
		if A.db_engine=='sqlite':A.db_connector=SqliteConnector(database_path=G)
		if A.db_engine=='wss':A.db_connector=WssConnector(socket_url=socket_url,dynamic_inputs=H,py_code_processing=I)
	def get_db_connector(A):return A.db_connector
	def test_connection(A):return A.db_connector.test_connection()
	def sparta_d6dc27c7ad(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)