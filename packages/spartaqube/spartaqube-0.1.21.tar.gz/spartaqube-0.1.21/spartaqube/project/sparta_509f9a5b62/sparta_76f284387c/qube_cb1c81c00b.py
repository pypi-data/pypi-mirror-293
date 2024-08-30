_D='manifest'
_C=None
_B=False
_A=True
import os,socket,json,requests
from datetime import date,datetime
from project.models import UserProfile,AppVersioning
from django.conf import settings as conf_settings
from spartaqube_app.secrets import sparta_4ae60e72f1
from project.sparta_12b080e841.sparta_63b2b3e72c.qube_cfdef982fe import sparta_47ae433e19
import pytz
UTC=pytz.utc
class dotdict(dict):__getattr__=dict.get;__setattr__=dict.__setitem__;__delattr__=dict.__delitem__
def sparta_cbc18a5346(appViewsModels):
	A=appViewsModels
	if isinstance(A,list):
		for C in A:
			for B in list(C.keys()):
				if isinstance(C[B],date):C[B]=str(C[B])
	else:
		for B in list(A.keys()):
			if isinstance(A[B],date):A[B]=str(A[B])
	return A
def sparta_bf6d63b430(thisText):A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=A+str('/log/log.txt');B=open(A,'a');B.write(thisText);B.writelines('\n');B.close()
def sparta_ae55297c84(request):A=request;return{'appName':'Project','user':A.user,'ip_address':A.META['REMOTE_ADDR']}
def sparta_945482f1af():return conf_settings.PLATFORM
def sparta_27c28cbb34():
	A=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));A=os.path.dirname(os.path.dirname(A))
	if conf_settings.DEBUG:C='static'
	else:C='staticfiles'
	E=A+f"/{C}/dist/manifest.json";F=open(E);B=json.load(F)
	if conf_settings.B_TOOLBAR:
		G=list(B.keys())
		for D in G:B[D]=A+f"/{C}"+B[D]
	return B
def sparta_aca8f1d9a9(request):
	B='';C=''
	if len(B)>0:B='/'+str(B)
	if len(C)>0:C='/'+str(C)
	try:
		A=_B;F=AppVersioning.objects.all();E=datetime.now().astimezone(UTC)
		if F.count()==0:AppVersioning.objects.create(last_check_date=E);A=_A
		else:
			D=F[0];G=D.last_check_date;H=E-G;I=sparta_47ae433e19();J=D.last_available_version_pip
			if not I==J:A=_A
			elif H.seconds>60*10:A=_A;D.last_check_date=E;D.save()
	except:A=_A
	K=conf_settings.HOST_WS_PREFIX;L=conf_settings.WEBSOCKET_PREFIX;M={'PROJECT_NAME':conf_settings.PROJECT_NAME,'CAPTCHA_SITEKEY':conf_settings.CAPTCHA_SITEKEY,'WEBSOCKET_PREFIX':L,'URL_PREFIX':B,'URL_WS_PREFIX':C,'HOST_WS_PREFIX':K,'CHECK_VERSIONING':A,'IS_DEV':conf_settings.IS_DEV,'IS_DOCKER':os.getenv('IS_REMOTE_SPARTAQUBE_CONTAINER','False')=='True'};return M
def sparta_8473884fda(captcha):
	D='errorMsg';B='res';A=captcha
	try:
		if A is not _C:
			if len(A)>0:
				E=sparta_4ae60e72f1()['CAPTCHA_SECRET_KEY'];F=f"https://www.google.com/recaptcha/api/siteverify?secret={E}&response={A}";C=requests.get(F)
				if int(C.status_code)==200:
					G=json.loads(C.text)
					if G['success']:return{B:1}
	except Exception as H:return{B:-1,D:str(H)}
	return{B:-1,D:'Invalid captcha'}
def sparta_0dd174178b(password):
	A=password;B=UserProfile.objects.filter(email=conf_settings.ADMIN_DEFAULT_EMAIL).all()
	if B.count()==0:return conf_settings.ADMIN_DEFAULT==A
	else:C=B[0];D=C.user;return D.check_password(A)
def sparta_5944c0222f(code):
	A=code
	try:
		if A is not _C:
			if len(A)>0:
				B=os.getenv('SPARTAQUBE_PASSWORD','admin')
				if B==A:return _A
	except:return _B
	return _B
def sparta_abf92cd2d9(user):
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
	A[_D]=sparta_27c28cbb34();return A
def sparta_3581b50e69(user):A=dict();A[_D]=sparta_27c28cbb34();return A
def sparta_5cf05d1b37():
	try:socket.create_connection(('1.1.1.1',53));return _A
	except OSError:pass
	return _B
def sparta_319e670c6b():A=socket.gethostname();B=socket.gethostbyname(A);return A,B