_C='json_api'
_B='postgres'
_A=None
import time,json,pandas as pd
from pandas.api.extensions import no_default
import project.sparta_12b080e841.sparta_c1258c27ef.qube_33c355412d as qube_33c355412d
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_00867b6890.qube_15bd90ab11 import ArcticConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_0920fb8502.qube_52c4ee771a import AerospikeConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_9b572f9ffe.qube_b67f06f337 import CassandraConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_04d1ed7791.qube_e21622d0a4 import ClickhouseConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_0fa787e0b1.qube_9ee37f1709 import CouchdbConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_21f6e6d768.qube_ffd27e129d import CsvConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_f7b34989a3.qube_7949a664e8 import DuckDBConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_854ab485b6.qube_491cdbdb37 import JsonApiConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_315dc351ce.qube_0a0962fb5f import InfluxdbConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_6032314d3e.qube_a12f20f00b import MariadbConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_4ca9c24e28.qube_ee0444e299 import MongoConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_b188c192d0.qube_47b3950196 import MssqlConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_1e0ff6a13e.qube_09bf1e51d7 import MysqlConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_77b1012478.qube_a3527f4c58 import OracleConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_9737c06dea.qube_cbeb73dc8a import ParquetConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_3acd13e80d.qube_7df361dc27 import PostgresConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_523539d523.qube_e8edbe76b9 import PythonConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_4fafe7f672.qube_3fee2b7a53 import QuestDBConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_8ea3a263e0.qube_8c4959ce15 import RedisConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_a6f96cc679.qube_6ed3bef57e import ScylladbConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_fea649e902.qube_8c42d0102d import SqliteConnector
from project.sparta_12b080e841.sparta_c1258c27ef.sparta_8ec4a93c0e.qube_91fde18776 import WssConnector
class Connector:
	def __init__(A,db_engine=_B):A.db_engine=db_engine
	def init_with_model(B,connector_obj):
		A=connector_obj;E=A.host;F=A.port;G=A.user;H=A.password_e
		try:C=qube_33c355412d.sparta_70515db35b(H)
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
	def sparta_5dc816a97d(A):return A.db_connector.preview_output_connector()
	def get_error_msg_test_connection(A):return A.db_connector.get_error_msg_test_connection()
	def get_available_tables(A):B=A.db_connector.get_available_tables();return B
	def get_table_columns(A,table_name):B=A.db_connector.get_table_columns(table_name);return B
	def get_data_table(A,table_name):
		if A.db_engine==_C:return A.db_connector.get_json_api_dataframe()
		else:B=A.db_connector.get_data_table(table_name);return pd.DataFrame(B)
	def get_data_table_query(A,sql,table_name=_A):return A.db_connector.get_data_table_query(sql,table_name=table_name)