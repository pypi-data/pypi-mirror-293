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
from project.sparta_12b080e841.sparta_fd283e4379 import qube_325cb84778 as qube_325cb84778
from project.sparta_12b080e841.sparta_d2a912facc import qube_fe01c20cda as qube_fe01c20cda
from project.sparta_12b080e841.sparta_580d8c46ca.qube_95c6ce3efb import sparta_c5ed4d9feb,sparta_d7410603aa
from project.sparta_12b080e841.sparta_580d8c46ca.qube_b16e15bcd6 import sparta_e7a5161547
from project.sparta_12b080e841.sparta_580d8c46ca.qube_b16e15bcd6 import sparta_ff50155928
def sparta_49923e7a42():keygen_fernet='spartaqube-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_f0cc9c3d2c():keygen_fernet='spartaqube-internal-decoder-api-key';key=keygen_fernet.encode(_B);key=hashlib.md5(key).hexdigest();key=base64.b64encode(key.encode(_B));return key.decode(_B)
def sparta_44a9cee88e(f,str_to_encrypt):data_to_encrypt=str_to_encrypt.encode(_B);token=f.encrypt(data_to_encrypt).decode(_B);token=base64.b64encode(token.encode(_B)).decode(_B);return token
def sparta_9495f9cf58(api_token_id):
	if api_token_id=='public':
		try:return User.objects.filter(username='public_spartaqube').all()[0]
		except:return
	try:
		f_private=Fernet(sparta_f0cc9c3d2c().encode(_B));api_key=f_private.decrypt(base64.b64decode(api_token_id)).decode(_B).split('@')[1];user_profile_set=UserProfile.objects.filter(api_key=api_key,is_banned=_D).all()
		if user_profile_set.count()==1:return user_profile_set[0].user
		return
	except Exception as e:print('Could not authenticate api with error msg:');print(e);return
def sparta_40c3634d14(json_data,user_obj):
	userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=userprofile_obj.api_key
	if api_key is _C:api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save()
	domain_name=json_data['domain'];random_nb=str(randint(0,1000));data_to_encrypt=f"apikey@{api_key}@{random_nb}";f_private=Fernet(sparta_f0cc9c3d2c().encode(_B));private_encryption=sparta_44a9cee88e(f_private,data_to_encrypt);data_to_encrypt=f"apikey@{domain_name}@{private_encryption}";f_public=Fernet(sparta_49923e7a42().encode(_B));public_encryption=sparta_44a9cee88e(f_public,data_to_encrypt);return{_A:1,'token':public_encryption}
def sparta_5225ba5c6c(json_data,user_obj):userprofile_obj=UserProfile.objects.get(user=user_obj);api_key=str(uuid.uuid4());userprofile_obj.api_key=api_key;userprofile_obj.save();return{_A:1}
def sparta_ed8abdcf7e():plot_types=sparta_e7a5161547();plot_types=sorted(plot_types,key=lambda x:x['Library'].lower(),reverse=_D);return{_A:1,'plot_types':plot_types}
def sparta_e46328d5fe(json_data):plot_type=json_data['plot_type'];plot_input_options_dict=sparta_ff50155928(plot_type);plot_input_options_dict[_A]=1;return plot_input_options_dict
def sparta_0bd6600841(code):
	tree=ast.parse(code)
	if isinstance(tree.body[-1],ast.Expr):last_expr_node=tree.body[-1].value;last_expr_code=ast.unparse(last_expr_node);return last_expr_code
	else:return
def sparta_b12485040c(json_data):
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
		print('EXECUTE API EXAMPLE DEBUG DEBUG DEBUG');print(user_code_example);exec(user_code_example,globals(),locals());last_expression_str=sparta_0bd6600841(user_code_example);print('last_expression_str');print(last_expression_str)
		if last_expression_str is not _C:
			last_expression_output=eval(last_expression_str)
			if last_expression_output.__class__.__name__=='HTML':resp=last_expression_output.data
			else:resp=last_expression_output
			print('last_expression_output');print(last_expression_output);resp=json.dumps(resp);print(resp);return{_A:1,'resp':resp,_E:error_msg}
		return{_A:-1,_E:'No output to display. You should put the variable to display as the last line of the code'}
	except Exception as e:return{_A:-1,_E:str(e)}
def sparta_6fe3def3a5(json_data,user_obj):
	session_id=json_data[_F];new_plot_api_variables_set=NewPlotApiVariables.objects.filter(session_id=session_id).all();print(f"gui_plot_api_variables with session_id {session_id}");print(new_plot_api_variables_set)
	if new_plot_api_variables_set.count()>0:
		new_plot_api_variables_obj=new_plot_api_variables_set[0];pickled_variables=new_plot_api_variables_obj.pickled_variables;unpickled_data=cloudpickle.loads(pickled_variables.encode('latin1'));notebook_variables=[]
		for notebook_variable in unpickled_data:
			notebook_variables_df=sparta_c5ed4d9feb(notebook_variable)
			if notebook_variables_df is not _C:0
			else:notebook_variables_df=pd.DataFrame()
			notebook_variables.append(sparta_d7410603aa(notebook_variables_df))
		print(notebook_variables);return{_A:1,_G:notebook_variables}
	return{_A:-1}
def sparta_f5d99446c1(json_data,user_obj):session_id=json_data[_F];notebook_cached_variables=qube_fe01c20cda.sparta_39a1db7371(session_id);return{_A:1,_G:notebook_cached_variables}
def sparta_fc122c71d7(json_data,user_obj):session_id=json_data[_F];return qube_fe01c20cda.sparta_e890c3e2c6(session_id)
def sparta_bb3f823bdc(json_data,user_obj):session_id=json_data[_F];widget_id=json_data['widgetId'];return qube_fe01c20cda.sparta_bb3f823bdc(user_obj,session_id,widget_id)
def sparta_7446ea5ae6(json_data,user_obj):
	api_service=json_data['api_service']
	if api_service=='get_status':output=sparta_ed683acd10()
	elif api_service=='get_connectors':return sparta_26f12eb721(json_data,user_obj)
	elif api_service=='get_connector_tables':return sparta_f756379bdb(json_data,user_obj)
	elif api_service=='get_data_from_connector':return sparta_352c9d17f7(json_data,user_obj)
	elif api_service=='get_widgets':output=sparta_c69898a043(user_obj)
	elif api_service=='has_widget_id':return sparta_e34bee1fea(json_data,user_obj)
	elif api_service=='get_widget_data':return sparta_c14ca017df(json_data,user_obj)
	elif api_service=='get_plot_types':return sparta_e7a5161547()
	elif api_service=='gui_plot_api_variables':return sparta_810b44b869(json_data,user_obj,b_check_type=_D)
	elif api_service=='plot_cache_variables':return sparta_810b44b869(json_data,user_obj)
	elif api_service=='clear_cache':return sparta_af17f7d6a9()
	return{_A:1,'output':output}
def sparta_ed683acd10():return 1
def sparta_26f12eb721(json_data,user_obj):
	A='db_connectors';keys_to_retain=['connector_id','name','db_engine'];res_dict=qube_fe01c20cda.sparta_fe498443ab(json_data,user_obj)
	if res_dict[_A]==1:res_dict[A]=[{k:d[k]for k in keys_to_retain if k in d}for d in res_dict[A]]
	return res_dict
def sparta_f756379bdb(json_data,user_obj):res_dict=qube_fe01c20cda.sparta_4e0ff641bf(json_data,user_obj);return res_dict
def sparta_352c9d17f7(json_data,user_obj):res_dict=qube_fe01c20cda.sparta_ed524b445e(json_data,user_obj);return res_dict
def sparta_c69898a043(user_obj):return qube_fe01c20cda.sparta_a9d18af5be(user_obj)
def sparta_e34bee1fea(json_data,user_obj):return qube_fe01c20cda.sparta_e34bee1fea(json_data,user_obj)
def sparta_c14ca017df(json_data,user_obj):return qube_fe01c20cda.sparta_a46f4aef67(json_data,user_obj)
def sparta_7c769485c0(json_data,user_obj):date_now=datetime.now().astimezone(UTC);session_id=str(uuid.uuid4());pickled_data=json_data['data'];NewPlotApiVariables.objects.create(user=user_obj,session_id=session_id,pickled_variables=pickled_data,date_created=date_now,last_update=date_now);return{_A:1,_H:session_id}
def sparta_ab8cb52a06():return sparta_e7a5161547()
def sparta_810b44b869(json_data,user_obj,b_check_type=True):
	A='cache_hash';variables_dict=json_data['variables']
	if b_check_type:
		chart_type_check=variables_dict['chart_type_check']
		if chart_type_check not in[elem['ID']for elem in sparta_e7a5161547()]:return{_A:-1,_E:'Invalid chart_type input'}
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
def sparta_af17f7d6a9():cache.clear();return{_A:1}