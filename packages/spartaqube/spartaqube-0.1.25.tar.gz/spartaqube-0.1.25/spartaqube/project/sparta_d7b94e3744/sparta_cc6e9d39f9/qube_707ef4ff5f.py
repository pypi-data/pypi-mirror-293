_D='manifest'
_C=None
_B=False
_A=True
import os,socket,json,requests
from datetime import date,datetime
from project.models import UserProfile,AppVersioning
from django.conf import settings as conf_settings
from spartaqube_app.secrets import sparta_543116a5ad
from project.sparta_40ba2b27bc.sparta_3c228a4852.qube_eae734e01a import sparta_b410aa5913
import pytz
UTC=pytz.utc
class dotdict(dict):__getattr__=dict.get;__setattr__=dict.__setitem__;__delattr__=dict.__delitem__
def sparta_217a4c5ca1(appViewsModels):
	A=appViewsModels
	if isinstance(A,list):
		for C in A:
			for B in list(C.keys()):
				if isinstance(C[B],date):C[B]=str(C[B])
	else:
		for B in list(A.keys()):
			if isinstance(A[B],date):A[B]=str(A[B])
	return A
def sparta_2aba052c6e(thisText):A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=A+str('/log/log.txt');B=open(A,'a');B.write(thisText);B.writelines('\n');B.close()
def sparta_8712b887c3(request):A=request;return{'appName':'Project','user':A.user,'ip_address':A.META['REMOTE_ADDR']}
def sparta_173d77a066():return conf_settings.PLATFORM
def sparta_e5a9460af8():
	A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=os.path.dirname(os.path.dirname(A))
	if conf_settings.DEBUG:C='static'
	else:C='staticfiles'
	E=A+f"/{C}/dist/manifest.json";F=open(E);B=json.load(F)
	if conf_settings.B_TOOLBAR:
		G=list(B.keys())
		for D in G:B[D]=A+f"/{C}"+B[D]
	return B
def sparta_d9406e4da5(request):
	B='';C=''
	if len(B)>0:B='/'+str(B)
	if len(C)>0:C='/'+str(C)
	try:
		A=_B;G=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if G.count()==0:AppVersioning.objects.create(last_check_date=E);A=_A
		else:
			D=G[0];H=D.last_check_date;I=E-H;J=sparta_b410aa5913();K=D.last_available_version_pip
			if not J==K:A=_A
			elif I.seconds>60*10:A=_A;D.last_check_date=E;D.save()
	except:A=_A
	F=-1
	if conf_settings.IS_DEV:0
	else:
		try:
			L=os.path.dirname(__file__);M=os.path.dirname(L);N=os.path.dirname(M);O=os.path.dirname(N);P=os.path.join(O,'api')
			with open(os.path.join(P,'app_data_asgi.json'),'r')as Q:R=json.load(Q)
			F=int(R['default_port'])
		except:F=5664
	S=conf_settings.HOST_WS_PREFIX;T=conf_settings.WEBSOCKET_PREFIX;U={'PROJECT_NAME':conf_settings.PROJECT_NAME,'CAPTCHA_SITEKEY':conf_settings.CAPTCHA_SITEKEY,'WEBSOCKET_PREFIX':T,'URL_PREFIX':B,'URL_WS_PREFIX':C,'ASGI_PORT':F,'HOST_WS_PREFIX':S,'CHECK_VERSIONING':A,'IS_DEV':conf_settings.IS_DEV,'IS_DOCKER':os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER','False')=='True'};return U
def sparta_4467781a0b(captcha):
	D='errorMsg';B='res';A=captcha
	try:
		if A is not _C:
			if len(A)>0:
				E=sparta_543116a5ad()['CAPTCHA_SECRET_KEY'];F=f"https://www.google.com/recaptcha/api/siteverify?secret={E}&response={A}";C=requests.get(F)
				if int(C.status_code)==200:
					G=json.loads(C.text)
					if G['success']:return{B:1}
	except Exception as H:return{B:-1,D:str(H)}
	return{B:-1,D:'Invalid captcha'}
def sparta_b0e7f57bbb(password):
	A=password;B=UserProfile.objects.filter(email=conf_settings.ADMIN_DEFAULT_EMAIL).all()
	if B.count()==0:return conf_settings.ADMIN_DEFAULT==A
	else:C=B[0];D=C.user;return D.check_password(A)
def sparta_b96de63680(code):
	A=code
	try:
		if A is not _C:
			if len(A)>0:
				B=os.getenv('SPARTAQUBE_PASSWORD','admin')
				if B==A:return _A
	except:return _B
	return _B
def sparta_d157c2d07e(user):
	F='default';A=dict()
	if not user.is_anonymous:
		E=UserProfile.objects.filter(user=user)
		if E.count()>0:
			B=E[0];D=B.avatar
			if D is not _C:D=B.avatar.avatar
			A['avatar']=D;A['userProfile']=B;C=B.editor_theme
			if C is _C:C=F
			elif len(C)==0:C=F
			else:C=B.editor_theme
			A['theme']=C;A['B_DARK_THEME']=B.is_dark_theme
	A[_D]=sparta_e5a9460af8();return A
def sparta_de19e1597e(user):A=dict();A[_D]=sparta_e5a9460af8();return A
def sparta_476a737eea():
	try:socket.create_connection(('1.1.1.1',53));return _A
	except OSError:pass
	return _B
def sparta_89632a0dae():A=socket.gethostname();B=socket.gethostbyname(A);return A,B