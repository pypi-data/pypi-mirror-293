_H='session_id'
_G='notebook_variables'
_F='session'
_E='errorMsg'
_D=False
_C=None
_B='utf-8'
_A='res'
import os,sys,json,ast,re,base64,uuid,hashlib,socket,cloudpickle,subprocess,threading
from random import randint
import pandas as pd
from cryptography.fernet import Fernet
from subprocess import PIPE
from datetime import datetime,timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.cache import cache
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared,CodeEditorNotebook
from project.models import ShareRights,UserProfile,NewPlotApiVariables
from project.sparta_30e2c8fafc.sparta_15e8153c5c import qube_65da3c3f33 as qube_65da3c3f33
from project.sparta_30e2c8fafc.sparta_2bc13df85d import qube_a1e444584f as qube_a1e444584f
from project.sparta_30e2c8fafc.sparta_e8608fa6bc.qube_e278700345 import sparta_389be66ef5,sparta_fb1f3aaed4
from project.sparta_30e2c8fafc.sparta_e8608fa6bc.qube_2d06db8025 import sparta_96a28d4f7b
from project.sparta_30e2c8fafc.sparta_e8608fa6bc.qube_2d06db8025 import sparta_8ff303dfd8
def sparta_dc8f796d8a():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_1fdb5f0d46():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_907862a5d9(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_7ae6d01ba2(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(email='public@spartaqube.com').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_1fdb5f0d46().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_22f25986e5(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_1fdb5f0d46().encode(_B));private_encryption=sparta_907862a5d9(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_dc8f796d8a().encode(_B));public_encryption=sparta_907862a5d9(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_ade5003b8f(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_48123c5064():plot_types=sparta_96a28d4f7b();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_e62a424901(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_8ff303dfd8(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_2fef93ec2f(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_b34e4cff53(json_data):
	user_code_example=json_data['userCode'];resp=_C;error_msg=''
	def is_port_available(port):
		try:
			with socket.socket(socket.AF_INET,socket.SOCK_STREAM)as s:s.bind(('localhost',port));return True
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
		print('EXECUTE API EXAMPLE DEBUG DEBUG DEBUG');print(user_code_example);exec(user_code_example,globals(),locals());last_expression_str=sparta_2fef93ec2f(user_code_example);print('last_expression_str');print(last_expression_str)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			print('last_expression_output');print(last_expression_output);resp=json.dumps(resp);print(resp);return{_A:1,'resp':resp,_E:error_msg}
		return{_A:-1,_E:'No output to display. You should put the variable to display as the last line of the code'}
	except Exception as e:return{_A:-1,_E:str(e)}
def sparta_70aa944df6(json_data,user_obj):
	session_id=json_data[_F];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_389be66ef5(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_fb1f3aaed4(notebook_variables_df))
		print(notebook_variables);return{_A:1,_G:notebook_variables}
	return{_A:-1}
def sparta_a235269d40(json_data,user_obj):session_id=json_data[_F];notebook_cached_variables=qube_a1e444584f.sparta_33c287c727(session_id);return{_A:1,_G:notebook_cached_variables}
def sparta_e6fb1d823a(json_data,user_obj):session_id=json_data[_F];return qube_a1e444584f.sparta_178f37e65d(session_id)
def sparta_1404d096dd(json_data,user_obj):session_id=json_data[_F];widget_id=json_data['widgetId'];return qube_a1e444584f.sparta_1404d096dd(user_obj,session_id,widget_id)
def sparta_b3b7dad7c2(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_d8217933de()
	elif api_service=='get_connectors':return sparta_6685886f05(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_537cd74da2(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_6a932580bf(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_84004d0fee(user_obj)
	elif api_service=='has_widget_id':return sparta_5235aeee84(json_data,user_obj)
	elif api_service=='get_widget_data':return sparta_6058bae8a1(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_96a28d4f7b()
	elif api_service=='gui_plot_api_variables':return sparta_beaaa71db7(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_beaaa71db7(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_ae98a80b8e()
	return{_A:1,'output':output}
def sparta_d8217933de():return 1
def sparta_6685886f05(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_a1e444584f.sparta_923e0026e1(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_537cd74da2(json_data,user_obj):res_dict=qube_a1e444584f.sparta_2028e57ccf(json_data,user_obj);return res_dict
def sparta_6a932580bf(json_data,user_obj):res_dict=qube_a1e444584f.sparta_96908f7898(json_data,user_obj);return res_dict
def sparta_84004d0fee(user_obj):return qube_a1e444584f.sparta_564b51f7f4(user_obj)
def sparta_5235aeee84(json_data,user_obj):return qube_a1e444584f.sparta_5235aeee84(json_data,user_obj)
def sparta_6058bae8a1(json_data,user_obj):return qube_a1e444584f.sparta_bc36cee727(json_data,user_obj)
def sparta_208db71b70(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_H:session_id}
def sparta_d0845b6063():return sparta_96a28d4f7b()
def sparta_beaaa71db7(json_data,user_obj,b_check_type=True):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_96a28d4f7b()]:return{_A:-1,_E:'Invalid chart_type input'}
	plot_params=json_data['plot_params'];all_hash_notebook=json_data['all_hash_notebook'];all_hash_server=json_data['all_hash_server'];b_missing_cache=_D
	for this_hash in all_hash_server:
		if cache.get(this_hash)is _C:b_missing_cache=True;break
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
	return{_A:1,_H:session_id,A:cache_hash}
def sparta_ae98a80b8e():cache.clear();return{_A:1}