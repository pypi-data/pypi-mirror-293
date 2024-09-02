_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_55934fbdfb.sparta_d2d53723e4.qube_6d51e15bd2 as qube_6d51e15bd2
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_527dceb576.qube_ee5ff209f4 import AerospikeConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_52c04a93eb.qube_5850561dba import CassandraConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_618dca04c0.qube_98ecc1dca1 import ClickhouseConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_92b4c8e9e1.qube_6cc479521f import CouchdbConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_37435381ec.qube_7f2ae000b2 import CsvConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_e5c0870e7a.qube_db8627f263 import DuckDBConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_9ea022783e.qube_0b1c89f7a8 import JsonApiConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_5866136c62.qube_bd4c6d6b9a import InfluxdbConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_ec1520aee2.qube_54ed346ad3 import MariadbConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_ea410646ac.qube_3d674b8ea9 import MongoConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_e2b505ae28.qube_5f0a10c980 import MssqlConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_dcadd699ac.qube_217be1d16e import MysqlConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_359297b8ac.qube_ab380bb771 import OracleConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_d2d363efd6.qube_5d1cfe3d9d import ParquetConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_ca6a5fa8de.qube_4462a6c244 import PostgresConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_0d7470e332.qube_103922e1b8 import PythonConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_5a66c6d179.qube_c525a6797b import QuestDBConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_8bc55f301e.qube_a97ecf4965 import RedisConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_13254d39fe.qube_ca862cf2b9 import ScylladbConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_8babf8be65.qube_7123a66279 import SqliteConnector
from project.sparta_55934fbdfb.sparta_d2d53723e4.sparta_ee492cf819.qube_236cea9ae1 import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_6d51e15bd2.sparta_446b1ef088(H)
		except:C=_A
		I=A.database;J=A.oracle_service_name;K=A.keyspace;L=A.library_arctic;M=A.database_path;N=A.read_only;O=A.json_url;P=A.socket_url;Q=A.db_engine;R=A.csv_path;S=A.csv_delimiter;T=A.token;U=A.organization;V=A.lib_dir;W=A.driver;X=A.trusted_connection;D=[]
		if A.dynamic_inputs is not _A:
			try:D=json.loads(A.dynamic_inputs)
			except:pass
		Y=A.py_code_processing;B.db_engine=Q;B.init_with_params(host=E,port=F,user=G,password=C,database=I,oracle_service_name=J,csv_path=R,csv_delimiter=S,keyspace=K,library_arctic=L,database_path=M,read_only=N,json_url=O,socket_url=P,dynamic_inputs=D,py_code_processing=Y,token=T,organization=U,lib_dir=V,driver=W,trusted_connection=X)
	def init_with_params(A,host,port,user=_A,password=_A,database=_A,oracle_service_name='orcl',csv_path=_A,csv_delimiter=_A,keyspace=_A,library_arctic=_A,database_path=_A,read_only=False,json_url=_A,socket_url=_A,redis_db=0,token=_A,organization=_A,lib_dir=_A,driver=_A,trusted_connection=True,dynamic_inputs=_A,py_code_processing=_A):
		J=keyspace;I=py_code_processing;H=dynamic_inputs;G=database_path;F=database;E=password;D=user;C=port;B=host;print('self.db_engine > '+str(A.db_engine))
		if A.db_engine=='aerospike':A.db_connector=AerospikeConnector(host=B,port=C,user=D,password=E,database=F)
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
	def sparta_e640e29f76(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)