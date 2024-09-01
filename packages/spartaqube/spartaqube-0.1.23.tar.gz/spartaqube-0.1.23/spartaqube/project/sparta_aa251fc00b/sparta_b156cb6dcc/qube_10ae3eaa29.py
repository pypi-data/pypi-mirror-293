_O='Please send valid data'
_N='dist/project/auth/resetPasswordChange.html'
_M='captcha'
_L='password'
_K='POST'
_J=False
_I='login'
_H='error'
_G='form'
_F='email'
_E='res'
_D='home'
_C='manifest'
_B='errorMsg'
_A=True
import json,hashlib,uuid
from datetime import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings as conf_settings
from django.urls import reverse
import project.sparta_9cf3fbfd16.sparta_527aa3c9b5.qube_8fc5e0b148 as qube_8fc5e0b148
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_7e621e226c
from project.sparta_30e2c8fafc.sparta_4f7fa902d8 import qube_b0ccd99581 as qube_b0ccd99581
from project.sparta_c575131ae1.sparta_cff862b572 import qube_731b4da362 as qube_731b4da362
from project.models import LoginLocation,UserProfile
def sparta_e52b0fd9c2():return{'bHasCompanyEE':-1}
def sparta_f64329dbc0(request):B=request;A=qube_8fc5e0b148.sparta_5c9f39e944(B);A[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_7e621e226c
def sparta_b0e30f091e(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_fccada985b(C,A)
def sparta_b9cda0b93b(request,redirectUrl):return sparta_fccada985b(request,redirectUrl)
def sparta_fccada985b(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_b0ccd99581.sparta_4ca170a814(F):return sparta_f64329dbc0(A)
				login(A,F);K,L=qube_8fc5e0b148.sparta_15baa16557();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_8fc5e0b148.sparta_5c9f39e944(A);B.update(qube_8fc5e0b148.sparta_123073b817(A));B[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_e52b0fd9c2());return render(A,'dist/project/auth/login.html',B)
def sparta_5285295642(request):
	B='public@spartaqube.com';A=authenticate(username=B,password='public')
	if A:login(request,A)
	return redirect(_D)
@sparta_7e621e226c
def sparta_a061fe8c9b(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_b0ccd99581.sparta_7b1e352200()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_b0ccd99581.sparta_dfafd23c9f(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_b0ccd99581.sparta_0cd5eb83b4(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_8fc5e0b148.sparta_5c9f39e944(A);C.update(qube_8fc5e0b148.sparta_123073b817(A));C[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_e52b0fd9c2());return render(A,'dist/project/auth/registration.html',C)
def sparta_8c7eda903f(request):A=request;B=qube_8fc5e0b148.sparta_5c9f39e944(A);B[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_98b3decf22(request,token):
	A=request;B=qube_b0ccd99581.sparta_44db7dfa5d(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_8fc5e0b148.sparta_5c9f39e944(A);D[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();return redirect(_I)
def sparta_48bd01f2f0(request):logout(request);return redirect(_I)
def sparta_aae6cbcf65(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_8448e86dd8(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_546e67c175(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_b0ccd99581.sparta_546e67c175(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_8fc5e0b148.sparta_5c9f39e944(A);C.update(qube_8fc5e0b148.sparta_123073b817(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_8fc5e0b148.sparta_5c9f39e944(A);D.update(qube_8fc5e0b148.sparta_123073b817(A));D[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_e52b0fd9c2());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_a921c4fb34(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_b0ccd99581.sparta_a921c4fb34(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_8fc5e0b148.sparta_5c9f39e944(D);A.update(qube_8fc5e0b148.sparta_123073b817(D));A[_C]=qube_8fc5e0b148.sparta_c8d8b3a618();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_e52b0fd9c2());return render(D,_N,A)