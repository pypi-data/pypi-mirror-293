import os,json,platform,websocket,threading,time,pandas as pd
from project.sparta_12b080e841.sparta_d2a912facc import qube_fe01c20cda as qube_fe01c20cda
from project.sparta_12b080e841.sparta_580d8c46ca.qube_95c6ce3efb import sparta_c5ed4d9feb
from project.sparta_12b080e841.sparta_c1258c27ef.qube_02af27a60d import Connector as Connector
IS_WINDOWS=False
if platform.system()=='Windows':IS_WINDOWS=True
from channels.generic.websocket import WebsocketConsumer
from project.sparta_509f9a5b62.sparta_76f284387c import qube_cb1c81c00b as qube_cb1c81c00b
from project.sparta_12b080e841.sparta_580d8c46ca import qube_95c6ce3efb as qube_95c6ce3efb
class WssConnectorWS(WebsocketConsumer):
	channel_session=True;http_user_and_session=True
	def connect(A):print('Connect Now');A.accept();A.user=A.scope['user'];A.json_data_dict=dict()
	def init_socket(B,json_data):
		A=json_data;D=A['is_model_connector'];B.connector_obj=Connector(db_engine='wss')
		if D:
			E=A['connector_id'];C=qube_fe01c20cda.sparta_5fc5d23807(E,B.user)
			if C is None:F={'res':-2,'errorMsg':'Invalid connector, please try again'};G=json.dumps(F);B.send(text_data=G);return
			B.connector_obj.init_with_model(C)
		else:B.connector_obj.init_with_params(host=A['host'],port=A['port'],user=A['user'],password=A['password'],database=A['database'],oracle_service_name=A['oracle_service_name'],csv_path=A['csv_path'],csv_delimiter=A['csv_delimiter'],keyspace=A['keyspace'],library_arctic=A['library_arctic'],database_path=A['database_path'],read_only=A['read_only'],json_url=A['json_url'],socket_url=A['socket_url'],redis_db=A['redis_db'],dynamic_inputs=A['dynamic_inputs'],py_code_processing=A['py_code_processing'])
		B.connector_obj.get_db_connector().start_stream(gui_websocket=B)
	def disconnect(A,close_code):
		print('Disconnect')
		try:A.connector_obj.get_db_connector().stop_threads()
		except:pass
	def receive(A,text_data):
		E='service';C=text_data
		if len(C)>0:
			D=json.loads(C);B=D[E]
			if B=='init-socket':A.init_socket(D);F={'res':1,E:B};G=json.dumps(F);A.send(text_data=G)
			if B=='stop-socket':A.connector_obj.get_db_connector().stop_stream(gui_websocket=A)