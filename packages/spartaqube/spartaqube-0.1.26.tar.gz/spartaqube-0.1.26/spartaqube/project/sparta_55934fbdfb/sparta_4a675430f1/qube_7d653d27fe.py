_J='session_id'
_I='output'
_H='notebook_variables'
_G='session'
_F='errorMsg'
_E=True
_D=False
_C=None
_B='utf-8'
_A='res'
import os,sys,json,ast,re,base64,uuid,hashlib,socket,cloudpickle,websocket,subprocess,threading
from random import randint
import pandas as pd
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
from django.conf import settings as conf_settings
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared,CodeEditorNotebook
from project.models import ShareRights,UserProfile,NewPlotApiVariables
from project.sparta_55934fbdfb.sparta_ed7297be8a import qube_73cd480ba9 as qube_73cd480ba9
from project.sparta_55934fbdfb.sparta_8d9d1db88d import qube_7c37f05664 as qube_7c37f05664
from project.sparta_55934fbdfb.sparta_ce3abe84ce.qube_e97887f5fc import sparta_9bc2dc9979,sparta_865a89042b
from project.sparta_55934fbdfb.sparta_ce3abe84ce.qube_a483a2fe5e import sparta_6b4a00247d
from project.sparta_55934fbdfb.sparta_ce3abe84ce.qube_a483a2fe5e import sparta_1e46ce512f
def sparta_23e18a63c2():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_bd6b71a495():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_b1b8d8d392(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_8e6096dfe6(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(email='public@spartaqube.com').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_bd6b71a495().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_a695d11c0d(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_bd6b71a495().encode(_B));private_encryption=sparta_b1b8d8d392(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_23e18a63c2().encode(_B));public_encryption=sparta_b1b8d8d392(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_1167431d8a(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_6104e58b03():plot_types=sparta_6b4a00247d();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_2adc3990fa(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_1e46ce512f(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_9552d930c9(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_2c881e6e7b(json_data):
	user_code_example=json_data['userCode'];resp=_C;error_msg=''
	def is_port_available(port):
		try:
			with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:s.bind(('localhost',port));return _E
		except socket.error:return _D
	def generate_port():
		port=8764
		while not is_port_available(port):port+=1
		return port
	def replace_spartaqube_port(text,port):text=re.sub('Spartaqube\\(\\)',f"Spartaqube(port={port})",text);text=re.sub('Spartaqube\\(port=\\d+\\)',f"Spartaqube(port={port})",text);return text
	def find_spartaqube_variable_names(text):
		pattern='(\\w+)\\s*=\\s*Spartaqube\\(.*?\\)';matches=re.findall(pattern,text)
		if len(matches)>0:return matches[0]
	try:
		print('EXECUTE API EXAMPLE DEBUG DEBUG DEBUG');print(user_code_example);exec(user_code_example,globals(),locals());last_expression_str=sparta_9552d930c9(user_code_example);print('last_expression_str');print(last_expression_str)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			print('last_expression_output');print(last_expression_output);resp=json.dumps(resp);print(resp);return{_A:1,'resp':resp,_F:error_msg}
		return{_A:-1,_F:'No output to display. You should put the variable to display as the last line of the code'}
	except Exception as e:return{_A:-1,_F:str(e)}
def sparta_414fa0127e(json_data,user_obj):
	session_id=json_data[_G];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_9bc2dc9979(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_865a89042b(notebook_variables_df))
		print(notebook_variables);return{_A:1,_H:notebook_variables}
	return{_A:-1}
def sparta_d081b41c82(json_data,user_obj):session_id=json_data[_G];notebook_cached_variables=qube_7c37f05664.sparta_657c72ac83(session_id);return{_A:1,_H:notebook_cached_variables}
def sparta_30bf04f9db(json_data,user_obj):session_id=json_data[_G];return qube_7c37f05664.sparta_e29e444c40(session_id)
def sparta_9c4dda4311(json_data,user_obj):session_id=json_data[_G];widget_id=json_data['widgetId'];return qube_7c37f05664.sparta_9c4dda4311(user_obj,session_id,widget_id)
def sparta_af0f122b64(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_d92f816210()
	elif api_service=='get_status_ws':return sparta_7e461e7def()
	elif api_service=='get_connectors':return sparta_3a9a83c471(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_ba6660235a(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_dbee0f742b(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_9adc0265fb(user_obj)
	elif api_service=='has_widget_id':return sparta_a206b39a62(json_data,user_obj)
	elif api_service=='get_widget_data':return sparta_7218cdeba0(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_6b4a00247d()
	elif api_service=='gui_plot_api_variables':return sparta_871d285f57(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_871d285f57(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_0f2f894dd5()
	return{_A:1,_I:output}
def sparta_d92f816210():return 1
def sparta_3a9a83c471(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_7c37f05664.sparta_fbb179184d(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_ba6660235a(json_data,user_obj):res_dict=qube_7c37f05664.sparta_b472d21afd(json_data,user_obj);return res_dict
def sparta_dbee0f742b(json_data,user_obj):res_dict=qube_7c37f05664.sparta_ab3b21dc94(json_data,user_obj);return res_dict
def sparta_9adc0265fb(user_obj):return qube_7c37f05664.sparta_625f42cd1a(user_obj)
def sparta_a206b39a62(json_data,user_obj):return qube_7c37f05664.sparta_a206b39a62(json_data,user_obj)
def sparta_7218cdeba0(json_data,user_obj):return qube_7c37f05664.sparta_5143b7af25(json_data,user_obj)
def sparta_9dc42ce022(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_J:session_id}
def sparta_4729f504b3():return sparta_6b4a00247d()
def sparta_871d285f57(json_data,user_obj,b_check_type=_E):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_6b4a00247d()]:return{_A:-1,_F:'Invalid chart_type input'}
	plot_params=json_data['plot_params'];all_hash_notebook=json_data['all_hash_notebook'];all_hash_server=json_data['all_hash_server'];b_missing_cache=_D
	for this_hash in all_hash_server:
		if cache.get(this_hash)is _C:b_missing_cache=_E;break
	if b_missing_cache:
		cache_hash=[]
		for this_hash in all_hash_notebook:
			if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
		return{_A:-1,'status_service':1,A:cache_hash}
	session_id=str(uuid.uuid4());cache.set(session_id,plot_params,timeout=_C)
	for(key,val)in variables_dict.items():
		if isinstance(val,dict):
			hash=val['hash'];hash_value_cache=cache.get(hash)
			if hash_value_cache is _C:hash_value_input=val.get('var',_C);cache.set(hash,hash_value_input,timeout=_C);print(f"Set hash {hash} for {key}")
	cache_hash=[]
	for this_hash in all_hash_notebook:
		if cache.get(this_hash)is not _C:cache_hash.append(this_hash)
	return{_A:1,_J:session_id,A:cache_hash}
def sparta_0f2f894dd5():cache.clear();return{_A:1}
def sparta_7e461e7def():
	global is_wss_valid;is_wss_valid=_D
	if conf_settings.IS_DEV:is_wss_valid=_E
	else:
		try:
			current_path=os.path.dirname(__file__);core_path=os.path.dirname(current_path);project_path=os.path.dirname(core_path);main_path=os.path.dirname(project_path);api_path=os.path.join(main_path,'api')
			with open(os.path.join(api_path,'app_data_asgi.json'),'r')as json_file:loaded_data_dict=json.load(json_file)
			ASGI_PORT=int(loaded_data_dict['default_port'])
		except:ASGI_PORT=5664
		def on_open(ws):global is_wss_valid;is_wss_valid=_E;ws.close()
		def on_error(ws,error):global is_wss_valid;is_wss_valid=_D;ws.close()
		def on_close(ws,close_status_code,close_msg):
			try:print(f"Connection closed with code: {close_status_code}, message: {close_msg}");ws.close()
			except Exception as e:print(f"Except: {e}")
		ws=websocket.WebSocketApp(f"ws://127.0.0.1:{ASGI_PORT}/ws/statusWS",on_open=on_open,on_close=on_close);ws.run_forever()
		if ws.sock and ws.sock.connected:print('WebSocket is still connected. Attempting to close again.');ws.close()
		else:print('WebSocket is properly closed.')
	return{_A:1,_I:is_wss_valid}