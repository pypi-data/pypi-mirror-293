_L='An error occurred, please try again'
_K='password_confirmation'
_J='password'
_I='jsonData'
_H='api_token_id'
_G='Invalid captcha'
_F='is_created'
_E='utf-8'
_D='errorMsg'
_C=False
_B=True
_A='res'
import hashlib,re,uuid,json,requests,socket,base64,traceback
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings as conf_settings
from django.urls import reverse
from project.models import UserProfile,GuestCode,GuestCodeGlobal,LocalApp,SpartaQubeCode
from project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b import sparta_8473884fda
from project.sparta_12b080e841.sparta_9a1d79032e import qube_aac46f9712 as qube_aac46f9712
from project.sparta_12b080e841.sparta_3736e9202c import qube_405fe6445a as qube_405fe6445a
from project.sparta_12b080e841.sparta_6d8df67f62.qube_c399594ca7 import Email as Email
def sparta_43a7ace2a8(function):
	def A(request,*E,**C):
		A=request;B=_B
		if not A.user.is_active:B=_C;logout(A)
		if not A.user.is_authenticated:B=_C;logout(A)
		if not B:
			D=C.get(_H)
			if D is not None:F=qube_405fe6445a.sparta_9495f9cf58(D);login(A,F)
		return function(A,*E,**C)
	return A
def sparta_47f2fcf87d(function):
	def A(request,*C,**D):
		B='notLoggerAPI';A=request
		if not A.user.is_active:return HttpResponseRedirect(reverse(B))
		if A.user.is_authenticated:return function(A,*C,**D)
		else:return HttpResponseRedirect(reverse(B))
	return A
def sparta_c480116748(function):
	def A(request,*B,**C):
		try:return function(request,*B,**C)
		except Exception as A:
			if conf_settings.DEBUG:print('Try catch exception with error:');print(A);print('traceback:');print(traceback.format_exc())
			D={_A:-1,_D:str(A)};E=json.dumps(D);return HttpResponse(E)
	return A
def sparta_70af082fea(function):
	C=function
	def A(request,*D,**E):
		A=request;F=_C
		try:
			G=json.loads(A.body);H=json.loads(G[_I]);I=H[_H];B=qube_405fe6445a.sparta_9495f9cf58(I)
			if B is not None:F=_B;A.user=B
		except Exception as J:print('exception pip auth');print(J)
		if F:return C(A,*D,**E)
		else:K='public@spartaqube.com';B=authenticate(username=K,password='public');A.user=B;return C(A,*D,**E)
	return A
def sparta_b4795b1424(code):
	try:
		B=SpartaQubeCode.objects.all()
		if B.count()==0:return code=='admin'
		else:C=B[0].spartaqube_code;A=hashlib.md5(code.encode(_E)).hexdigest();A=base64.b64encode(A.encode(_E));A=A.decode(_E);return A==C
	except Exception as D:pass
	return _C
def sparta_abba9de946():
	A=LocalApp.objects.all()
	if A.count()==0:B=str(uuid.uuid4());LocalApp.objects.create(app_id=B,date_created=datetime.now());return B
	else:return A[0].app_id
def sparta_07be43f9f2():A=socket.gethostname();B=socket.gethostbyname(A);return B
def sparta_af3b86afda(json_data):
	D='ip_addr';A=json_data;del A[_J];del A[_K]
	try:A[D]=sparta_07be43f9f2()
	except:A[D]=-1
	C=dict();C[_I]=json.dumps(A);B=requests.post(f"{conf_settings.SPARTAQUBE_WEBSITE}/create-user",data=json.dumps(C))
	if B.status_code==200:
		try:
			A=json.loads(B.text)
			if A[_A]==1:return{_A:1,_F:_B}
			else:A[_F]=_C;return A
		except Exception as E:return{_A:-1,_F:_C,_D:str(E)}
	return{_A:1,_F:_C,_D:f"status code: {B.status_code}. Please check your internet connection"}
def sparta_37784e484f(json_data,hostname_url):
	P='emailExist';O='passwordConfirm';K='email';B=json_data;F={O:'The two passwords must be the same...',K:'Email address is not valid...','form':'The form you sent is not valid...',P:'This email is already registered...'};E=_C;Q=B['firstName'].capitalize();R=B['lastName'].capitalize();C=B[K].lower();L=B[_J];S=B[_K];T=B['code'];M=B['captcha'];B['app_id']=sparta_abba9de946()
	if M=='cypress'and C=='cypress_tests@gmail.com':0
	else:
		U=sparta_8473884fda(M)
		if U[_A]!=1:return{_A:-1,_D:_G}
	if not sparta_b4795b1424(T):return{_A:-1,_D:'Invalid spartaqube code, please contact your administrator'}
	if L!=S:E=_B;G=F[O]
	if not re.match('[^@]+@[^@]+\\.[^@]+',C):E=_B;G=F[K]
	if User.objects.filter(username=C).exists():E=_B;G=F[P]
	if not E:
		V=sparta_af3b86afda(B);N=_B;W=V[_F]
		if not W:N=_C
		A=User.objects.create_user(C,C,L);A.is_staff=_C;A.username=C;A.first_name=Q;A.last_name=R;A.is_active=_B;A.save();D=UserProfile(user=A);H=str(A.id)+'_'+str(A.email);H=H.encode(_E);I=hashlib.md5(H).hexdigest()+str(datetime.now());I=I.encode(_E);X=str(uuid.uuid4());D.user_profile_id=hashlib.sha256(I).hexdigest();D.email=C;D.api_key=str(uuid.uuid4());D.registration_token=X;D.b_created_website=N;D.save();J={_A:1,'userObj':A};return J
	J={_A:-1,_D:G};return J
def sparta_b3a7f44ad9(user_obj,hostname_url,registration_token):C='Validate your account';B=user_obj;A=Email(B.username,[B.email],f"Welcome to {conf_settings.PROJECT_NAME}",C);A.addOneRow(C);A.addSpaceSeparator();A.addOneRow('Click on the link below to validate your account');D=f"{hostname_url.rstrip('/')}/registration-validation/{registration_token}";A.addOneCenteredButton('Validate',D);A.send()
def sparta_33bc22b986(token):
	C=UserProfile.objects.filter(registration_token=token)
	if C.count()>0:A=C[0];A.registration_token='';A.is_account_validated=_B;A.save();B=A.user;B.is_active=_B;B.save();return{_A:1,'user':B}
	return{_A:-1,_D:'Invalid registration token'}
def sparta_adb781fcdb():return conf_settings.IS_GUEST_CODE_REQUIRED
def sparta_f933cf0a2c(guest_code):
	if GuestCodeGlobal.objects.filter(guest_id=guest_code,is_active=_B).count()>0:return _B
	return _C
def sparta_723edc23f6(guest_code,user_obj):
	D=user_obj;C=guest_code
	if GuestCodeGlobal.objects.filter(guest_id=C,is_active=_B).count()>0:return _B
	A=GuestCode.objects.filter(user=D)
	if A.count()>0:return _B
	else:
		A=GuestCode.objects.filter(guest_id=C,is_used=_C)
		if A.count()>0:B=A[0];B.user=D;B.is_used=_B;B.save();return _B
	return _C
def sparta_80f3732371(user):
	A=UserProfile.objects.filter(user=user)
	if A.count()==1:return A[0].is_banned
	else:return _C
def sparta_3e7d1ae01a(email,captcha):
	D=sparta_8473884fda(captcha)
	if D[_A]!=1:return{_A:-1,_D:_G}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_L}
	A=B[0];C=str(uuid.uuid4());A.token_reset_password=C;A.save();sparta_b9221a6f6d(A.user,C);return{_A:1}
def sparta_b9221a6f6d(user_obj,token_reset_password):B=user_obj;A=Email(B.username,[B.email],'Reset Password','Reset Password Message');A.addOneRow('Reset code','Copy the following code to reset your password');A.addSpaceSeparator();A.addOneRow(token_reset_password);A.send()
def sparta_25268276d3(captcha,token,email,password):
	D=sparta_8473884fda(captcha)
	if D[_A]!=1:return{_A:-1,_D:_G}
	B=UserProfile.objects.filter(user__username=email)
	if B.count()==0:return{_A:-1,_D:_L}
	A=B[0]
	if not token==A.token_reset_password:return{_A:-1,_D:'Invalid token..., please try again'}
	A.token_reset_password='';A.save();C=A.user;C.set_password(password);C.save();return{_A:1}