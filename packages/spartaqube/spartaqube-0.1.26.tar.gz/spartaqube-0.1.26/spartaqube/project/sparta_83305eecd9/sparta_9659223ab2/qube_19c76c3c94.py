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
import project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 as qube_4982ec8d00
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_091e7a614b
from project.sparta_55934fbdfb.sparta_db8b2eb16f import qube_da95fe36a3 as qube_da95fe36a3
from project.sparta_7ca3ee6127.sparta_5f839448b3 import qube_120ae90c07 as qube_120ae90c07
from project.models import LoginLocation,UserProfile
def sparta_f89886cc62():return{'bHasCompanyEE':-1}
def sparta_26eab0a9e9(request):B=request;A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A[_C]=qube_4982ec8d00.sparta_1fd141aa50();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_091e7a614b
def sparta_f22f181c21(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_33061a88a0(C,A)
def sparta_430ec8e78c(request,redirectUrl):return sparta_33061a88a0(request,redirectUrl)
def sparta_33061a88a0(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_da95fe36a3.sparta_5ad8bf48b5(F):return sparta_26eab0a9e9(A)
				login(A,F);K,L=qube_4982ec8d00.sparta_a43e70f682();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_4982ec8d00.sparta_48cfdf4b1d(A);B.update(qube_4982ec8d00.sparta_1f2805a4b9(A));B[_C]=qube_4982ec8d00.sparta_1fd141aa50();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_f89886cc62());return render(A,'dist/project/auth/login.html',B)
def sparta_f74e588e07(request):
	B='public@spartaqube.com';A=authenticate(username=B,password='public')
	if A:login(request,A)
	return redirect(_D)
@sparta_091e7a614b
def sparta_97f53dc95b(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_da95fe36a3.sparta_be3ec3bff5()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_da95fe36a3.sparta_811ebe5391(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_da95fe36a3.sparta_dbac5e9c95(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_4982ec8d00.sparta_48cfdf4b1d(A);C.update(qube_4982ec8d00.sparta_1f2805a4b9(A));C[_C]=qube_4982ec8d00.sparta_1fd141aa50();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_f89886cc62());return render(A,'dist/project/auth/registration.html',C)
def sparta_7bfe842791(request):A=request;B=qube_4982ec8d00.sparta_48cfdf4b1d(A);B[_C]=qube_4982ec8d00.sparta_1fd141aa50();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_d0cf6bb5e8(request,token):
	A=request;B=qube_da95fe36a3.sparta_4f976a3885(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_4982ec8d00.sparta_48cfdf4b1d(A);D[_C]=qube_4982ec8d00.sparta_1fd141aa50();return redirect(_I)
def sparta_2036d4988f(request):logout(request);return redirect(_I)
def sparta_a2965c83ab(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_be96abe252(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_d93b29300c(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_da95fe36a3.sparta_d93b29300c(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_4982ec8d00.sparta_48cfdf4b1d(A);C.update(qube_4982ec8d00.sparta_1f2805a4b9(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_4982ec8d00.sparta_1fd141aa50();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_4982ec8d00.sparta_48cfdf4b1d(A);D.update(qube_4982ec8d00.sparta_1f2805a4b9(A));D[_C]=qube_4982ec8d00.sparta_1fd141aa50();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_f89886cc62());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_7bb7bff37c(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_da95fe36a3.sparta_7bb7bff37c(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_4982ec8d00.sparta_48cfdf4b1d(D);A.update(qube_4982ec8d00.sparta_1f2805a4b9(D));A[_C]=qube_4982ec8d00.sparta_1fd141aa50();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_f89886cc62());return render(D,_N,A)