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
from project.sparta_40ba2b27bc.sparta_b467cb3ea8 import qube_3228fef6bb as qube_3228fef6bb
from project.sparta_40ba2b27bc.sparta_ffa6b80cbc import qube_8c9113b621 as qube_8c9113b621
from project.sparta_40ba2b27bc.sparta_dc05d02cc2.qube_0377b9b446 import sparta_4cc463fb2a,sparta_64d58aadc8
from project.sparta_40ba2b27bc.sparta_dc05d02cc2.qube_5dfa60af91 import sparta_5f86688418
from project.sparta_40ba2b27bc.sparta_dc05d02cc2.qube_5dfa60af91 import sparta_530358642d
def sparta_cf8e6b5c67():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_062e505b1d():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_44b4d84156(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_f9172ac474(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(email='public@spartaqube.com').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_062e505b1d().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_6dcb05fdc5(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_062e505b1d().encode(_B));private_encryption=sparta_44b4d84156(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_cf8e6b5c67().encode(_B));public_encryption=sparta_44b4d84156(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_f7eb2276a5(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_2b38d9b249():plot_types=sparta_5f86688418();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_1b0729553f(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_530358642d(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_a2987c12bf(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_52b3cbb396(json_data):
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
		print('EXECUTE API EXAMPLE DEBUG DEBUG DEBUG');print(user_code_example);exec(user_code_example,globals(),locals());last_expression_str=sparta_a2987c12bf(user_code_example);print('last_expression_str');print(last_expression_str)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			print('last_expression_output');print(last_expression_output);resp=json.dumps(resp);print(resp);return{_A:1,'resp':resp,_F:error_msg}
		return{_A:-1,_F:'No output to display. You should put the variable to display as the last line of the code'}
	except Exception as e:return{_A:-1,_F:str(e)}
def sparta_ba1fdc9948(json_data,user_obj):
	session_id=json_data[_G];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_4cc463fb2a(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_64d58aadc8(notebook_variables_df))
		print(notebook_variables);return{_A:1,_H:notebook_variables}
	return{_A:-1}
def sparta_a68abd24ff(json_data,user_obj):session_id=json_data[_G];notebook_cached_variables=qube_8c9113b621.sparta_3bdc4e756c(session_id);return{_A:1,_H:notebook_cached_variables}
def sparta_669abefd23(json_data,user_obj):session_id=json_data[_G];return qube_8c9113b621.sparta_102f77f2c1(session_id)
def sparta_6cbaa07ff6(json_data,user_obj):session_id=json_data[_G];widget_id=json_data['widgetId'];return qube_8c9113b621.sparta_6cbaa07ff6(user_obj,session_id,widget_id)
def sparta_16409814c8(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_0316566a9f()
	elif api_service=='get_status_ws':return sparta_9af7a7e369()
	elif api_service=='get_connectors':return sparta_460921bcad(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_59fb0d0bdf(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_6e31dd73fe(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_47e1eff039(user_obj)
	elif api_service=='has_widget_id':return sparta_0ac0753e77(json_data,user_obj)
	elif api_service=='get_widget_data':return sparta_c488212d8b(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_5f86688418()
	elif api_service=='gui_plot_api_variables':return sparta_e4b74381db(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_e4b74381db(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_e1ec7ea39e()
	return{_A:1,_I:output}
def sparta_0316566a9f():return 1
def sparta_460921bcad(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_8c9113b621.sparta_921b5d9da3(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_59fb0d0bdf(json_data,user_obj):res_dict=qube_8c9113b621.sparta_47a15f51ae(json_data,user_obj);return res_dict
def sparta_6e31dd73fe(json_data,user_obj):res_dict=qube_8c9113b621.sparta_683b39c9f6(json_data,user_obj);return res_dict
def sparta_47e1eff039(user_obj):return qube_8c9113b621.sparta_b4f3a67669(user_obj)
def sparta_0ac0753e77(json_data,user_obj):return qube_8c9113b621.sparta_0ac0753e77(json_data,user_obj)
def sparta_c488212d8b(json_data,user_obj):return qube_8c9113b621.sparta_1dcc8adbe2(json_data,user_obj)
def sparta_a35ea2daef(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_J:session_id}
def sparta_247cb1fa49():return sparta_5f86688418()
def sparta_e4b74381db(json_data,user_obj,b_check_type=_E):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_5f86688418()]:return{_A:-1,_F:'Invalid chart_type input'}
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
def sparta_e1ec7ea39e():cache.clear();return{_A:1}
def sparta_9af7a7e369():
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