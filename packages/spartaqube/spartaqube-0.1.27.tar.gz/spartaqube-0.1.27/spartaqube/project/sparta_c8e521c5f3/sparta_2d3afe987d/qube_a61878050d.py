_A='utf-8'
import base64,hashlib
from cryptography.fernet import Fernet
def sparta_6b26d38a0b():B='db-conn';A=B.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A.decode(_A)
def sparta_acabf12e6f(password_to_encrypt):A=password_to_encrypt;A=A.encode(_A);C=Fernet(sparta_6b26d38a0b().encode(_A));B=C.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_54b9f4645f(password_e):B=Fernet(sparta_6b26d38a0b().encode(_A));A=base64.b64decode(password_e);A=B.decrypt(A).decode(_A);return A
def sparta_3cdd98a293():return sorted(['aerospike','cassandra','clickhouse','couchdb','csv','duckdb','influxdb','json_api','mariadb','mongo','mssql','mysql','oracle','parquet','postgres','python','questdb','redis','scylladb','sqlite','wss'])