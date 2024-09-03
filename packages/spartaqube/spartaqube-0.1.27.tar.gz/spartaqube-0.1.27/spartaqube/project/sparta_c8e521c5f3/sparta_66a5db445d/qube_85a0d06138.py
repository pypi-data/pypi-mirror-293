import json,base64,asyncio,subprocess,uuid,requests,pandas as pd
from subprocess import PIPE
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
UTC=pytz.utc
from project.models_spartaqube import DBConnector,DBConnectorUserShared,PlotDBChart,PlotDBChartShared
from project.models import ShareRights
from project.sparta_c8e521c5f3.sparta_712aa01975 import qube_05804de984 as qube_05804de984
from project.sparta_c8e521c5f3.sparta_2d3afe987d import qube_a61878050d
from project.sparta_c8e521c5f3.sparta_1506e63207 import qube_e74e1c855f as qube_e74e1c855f
from project.sparta_c8e521c5f3.sparta_2d3afe987d.qube_7cbb653792 import Connector as Connector
def sparta_9b3691b2e9(json_data,user_obj):
	D='key';A=json_data;print('Call autocompelte api');print(A);B=A[D];E=A['api_func'];C=[]
	if E=='tv_symbols':C=sparta_58e4f7bbfa(B)
	return{'res':1,'output':C,D:B}
def sparta_58e4f7bbfa(key_symbol):
	F='</em>';E='<em>';B='symbol_id';G=f"https://symbol-search.tradingview.com/local_search/v3/?text={key_symbol}&hl=1&exchange=&lang=en&search_type=undefined&domain=production&sort_by_country=US";C=requests.get(G)
	try:
		if int(C.status_code)==200:
			H=json.loads(C.text);D=H['symbols']
			for A in D:A[B]=A['symbol'].replace(E,'').replace(F,'');A['title']=A[B];A['subtitle']=A['description'].replace(E,'').replace(F,'');A['value']=A[B]
			return D
		return[]
	except:return[]