_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_c8e521c5f3.sparta_2d3afe987d.qube_a61878050d as qube_a61878050d
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_f7a38fe272.qube_389c470024 import AerospikeConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_59ba51ab74.qube_034e7e8bdb import CassandraConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_9a8f79ec83.qube_ac38b2f9af import ClickhouseConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_f2abb121e8.qube_30baec58f2 import CouchdbConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_c1af1eb6d1.qube_1784c26fd7 import CsvConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_90b4595574.qube_ff7070fc3a import DuckDBConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_8e9bf43bbd.qube_c3d1296cf5 import JsonApiConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_16a9228343.qube_05e2b80481 import InfluxdbConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_9689f8aaf2.qube_9d0fc1b22c import MariadbConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_c03cae5077.qube_cb2b4556aa import MongoConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_c084bac4b0.qube_27ad387409 import MssqlConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_6453a7d0f4.qube_f620edd85f import MysqlConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_af0afa5bbf.qube_9771bf5c54 import OracleConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_8ee3d16415.qube_c113e32b4a import ParquetConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_37b95a3314.qube_53b038665f import PostgresConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_ae7e62e844.qube_f1ddf86fe4 import PythonConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_8cd11eac99.qube_6fc9e406f2 import QuestDBConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_9b0ef5b2c0.qube_c8f8319207 import RedisConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_d6ac384dee.qube_8c834823e8 import ScylladbConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_7b6eb93982.qube_787c6cb9cb import SqliteConnector
from project.sparta_c8e521c5f3.sparta_2d3afe987d.sparta_43de4b707e.qube_8a82b19d0e import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_a61878050d.sparta_54b9f4645f(H)
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
	def sparta_d97b6e3798(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)