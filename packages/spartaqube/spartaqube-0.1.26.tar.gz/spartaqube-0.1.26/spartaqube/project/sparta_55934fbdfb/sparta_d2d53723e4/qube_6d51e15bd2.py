_A='utf-8'
import base64,hashlib
from cryptography.fernet import Fernet
def sparta_fac8c680ee():B='db-conn';A=B.encode(_A);A=hashlib.md5(A).hexdigest();A=base64.b64encode(A.encode(_A));return A.decode(_A)
def sparta_a9a113348c(password_to_encrypt):A=password_to_encrypt;A=A.encode(_A);C=Fernet(sparta_fac8c680ee().encode(_A));B=C.encrypt(A).decode(_A);B=base64.b64encode(B.encode(_A)).decode(_A);return B
def sparta_446b1ef088(password_e):B=Fernet(sparta_fac8c680ee().encode(_A));A=base64.b64decode(password_e);A=B.decrypt(A).decode(_A);return A
def sparta_5646f35edb():return sorted(['aerospike','cassandra','clickhouse','couchdb','csv','duckdb','influxdb','json_api','mariadb','mongo','mssql','mysql','oracle','parquet','postgres','python','questdb','redis','scylladb','sqlite','wss'])