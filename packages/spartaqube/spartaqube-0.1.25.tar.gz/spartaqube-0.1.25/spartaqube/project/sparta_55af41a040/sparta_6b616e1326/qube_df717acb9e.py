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
import project.sparta_d7b94e3744.sparta_cc6e9d39f9.qube_707ef4ff5f as qube_707ef4ff5f
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_42f3fead5c
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8 import qube_816b9a59f8 as qube_816b9a59f8
from project.sparta_f87b61a7bd.sparta_2ad048398d import qube_51126b7bc6 as qube_51126b7bc6
from project.models import LoginLocation,UserProfile
def sparta_dc31a2f3a5():return{'bHasCompanyEE':-1}
def sparta_7a5c6ed1eb(request):B=request;A=qube_707ef4ff5f.sparta_d9406e4da5(B);A[_C]=qube_707ef4ff5f.sparta_e5a9460af8();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_42f3fead5c
def sparta_e48c75941e(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_f400bc68ed(C,A)
def sparta_f0c4273b22(request,redirectUrl):return sparta_f400bc68ed(request,redirectUrl)
def sparta_f400bc68ed(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_816b9a59f8.sparta_a5ff51ff38(F):return sparta_7a5c6ed1eb(A)
				login(A,F);K,L=qube_707ef4ff5f.sparta_89632a0dae();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_707ef4ff5f.sparta_d9406e4da5(A);B.update(qube_707ef4ff5f.sparta_8712b887c3(A));B[_C]=qube_707ef4ff5f.sparta_e5a9460af8();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_dc31a2f3a5());return render(A,'dist/project/auth/login.html',B)
def sparta_46038a5559(request):
	B='public@spartaqube.com';A=authenticate(username=B,password='public')
	if A:login(request,A)
	return redirect(_D)
@sparta_42f3fead5c
def sparta_c837ec89dd(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_816b9a59f8.sparta_33b4fa5814()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_816b9a59f8.sparta_b0803f4cc1(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_816b9a59f8.sparta_40ebc608c0(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_707ef4ff5f.sparta_d9406e4da5(A);C.update(qube_707ef4ff5f.sparta_8712b887c3(A));C[_C]=qube_707ef4ff5f.sparta_e5a9460af8();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_dc31a2f3a5());return render(A,'dist/project/auth/registration.html',C)
def sparta_2fae21984d(request):A=request;B=qube_707ef4ff5f.sparta_d9406e4da5(A);B[_C]=qube_707ef4ff5f.sparta_e5a9460af8();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_c81900a9ea(request,token):
	A=request;B=qube_816b9a59f8.sparta_1b338bb89a(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_707ef4ff5f.sparta_d9406e4da5(A);D[_C]=qube_707ef4ff5f.sparta_e5a9460af8();return redirect(_I)
def sparta_0e6f4d8dac(request):logout(request);return redirect(_I)
def sparta_eff0f6d676(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_4316787b56(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_8c86a23d26(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_816b9a59f8.sparta_8c86a23d26(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_707ef4ff5f.sparta_d9406e4da5(A);C.update(qube_707ef4ff5f.sparta_8712b887c3(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_707ef4ff5f.sparta_e5a9460af8();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_707ef4ff5f.sparta_d9406e4da5(A);D.update(qube_707ef4ff5f.sparta_8712b887c3(A));D[_C]=qube_707ef4ff5f.sparta_e5a9460af8();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_dc31a2f3a5());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_b08e588df7(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_816b9a59f8.sparta_b08e588df7(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_707ef4ff5f.sparta_d9406e4da5(D);A.update(qube_707ef4ff5f.sparta_8712b887c3(D));A[_C]=qube_707ef4ff5f.sparta_e5a9460af8();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_dc31a2f3a5());return render(D,_N,A)