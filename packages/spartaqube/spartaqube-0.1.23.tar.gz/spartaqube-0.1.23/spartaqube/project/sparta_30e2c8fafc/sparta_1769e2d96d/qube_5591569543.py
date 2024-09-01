import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_30e2c8fafc.sparta_15e8153c5c import qube_65da3c3f33 as qube_65da3c3f33
from project.sparta_30e2c8fafc.sparta_e8f9e9d192 import qube_84ad741dd2
from project.sparta_30e2c8fafc.sparta_2bc13df85d import qube_720376529a as qube_720376529a
from project.sparta_30e2c8fafc.sparta_e8f9e9d192.qube_7ccbcc1e17 import Connector as Connector
def sparta_fa9f4867a7(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_dd4c88f142(B)
	return{'res':1,'output':C,D:B}
def sparta_dd4c88f142(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]