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
import project.sparta_3ca0064d9b.sparta_e277eee10c.qube_b6b724ff27 as qube_b6b724ff27
from project.forms import ConnexionForm,RegistrationTestForm,RegistrationBaseForm,RegistrationForm,ResetPasswordForm,ResetPasswordChangeForm
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_25d3a2863e
from project.sparta_c8e521c5f3.sparta_bc89190359 import qube_6059f885cd as qube_6059f885cd
from project.sparta_ea984c09ce.sparta_d3f2e3c139 import qube_e8db5816fe as qube_e8db5816fe
from project.models import LoginLocation,UserProfile
def sparta_7c21b26e3e():return{'bHasCompanyEE':-1}
def sparta_db724c456a(request):B=request;A=qube_b6b724ff27.sparta_673b1c1989(B);A[_C]=qube_b6b724ff27.sparta_e6aecc704c();A['forbiddenEmail']=conf_settings.FORBIDDEN_EMAIL;return render(B,'dist/project/auth/banned.html',A)
@sparta_25d3a2863e
def sparta_f6d44e2529(request):
	C=request;B='/';A=C.GET.get(_I)
	if A is not None:D=A.split(B);A=B.join(D[1:]);A=A.replace(B,'$@$')
	return sparta_f55a9a2891(C,A)
def sparta_9d94f03a45(request,redirectUrl):return sparta_f55a9a2891(request,redirectUrl)
def sparta_f55a9a2891(request,redirectUrl):
	E=redirectUrl;A=request;print('Welcome to loginRedirectFunc')
	if A.user.is_authenticated:return redirect(_D)
	G=_J;H='Email or password incorrect'
	if A.method==_K:
		C=ConnexionForm(A.POST)
		if C.is_valid():
			I=C.cleaned_data[_F];J=C.cleaned_data[_L];F=authenticate(username=I,password=J)
			if F:
				if qube_6059f885cd.sparta_142b5154a7(F):return sparta_db724c456a(A)
				login(A,F);K,L=qube_b6b724ff27.sparta_ac7044c75b();LoginLocation.objects.create(user=F,hostname=K,ip=L,date_login=datetime.now())
				if E is not None:
					D=E.split('$@$');D=[A for A in D if len(A)>0]
					if len(D)>1:M=D[0];return redirect(reverse(M,args=D[1:]))
					return redirect(E)
				return redirect(_D)
			else:G=_A
		else:G=_A
	C=ConnexionForm();B=qube_b6b724ff27.sparta_673b1c1989(A);B.update(qube_b6b724ff27.sparta_2e9aa9b15f(A));B[_C]=qube_b6b724ff27.sparta_e6aecc704c();B[_G]=C;B[_H]=G;B['redirectUrl']=E;B[_B]=H;B.update(sparta_7c21b26e3e());return render(A,'dist/project/auth/login.html',B)
def sparta_0221666899(request):
	B='public@spartaqube.com';A=User.objects.filter(email=B).all()
	if A.count()>0:C=A[0];login(request,C)
	return redirect(_D)
@sparta_25d3a2863e
def sparta_8dfc038b03(request):
	A=request
	if A.user.is_authenticated:return redirect(_D)
	E='';D=_J;F=qube_6059f885cd.sparta_7c7a42d896()
	if A.method==_K:
		if F:B=RegistrationForm(A.POST)
		else:B=RegistrationBaseForm(A.POST)
		if B.is_valid():
			I=B.cleaned_data;H=None
			if F:
				H=B.cleaned_data['code']
				if not qube_6059f885cd.sparta_b7c0bfe7cf(H):D=_A;E='Wrong guest code'
			if not D:
				J=A.META['HTTP_HOST'];G=qube_6059f885cd.sparta_5a1cd67310(I,J)
				if int(G[_E])==1:K=G['userObj'];login(A,K);return redirect(_D)
				else:D=_A;E=G[_B]
		else:D=_A;E=B.errors.as_data()
	if F:B=RegistrationForm()
	else:B=RegistrationBaseForm()
	C=qube_b6b724ff27.sparta_673b1c1989(A);C.update(qube_b6b724ff27.sparta_2e9aa9b15f(A));C[_C]=qube_b6b724ff27.sparta_e6aecc704c();C[_G]=B;C[_H]=D;C[_B]=E;C.update(sparta_7c21b26e3e());return render(A,'dist/project/auth/registration.html',C)
def sparta_a12eb94206(request):A=request;B=qube_b6b724ff27.sparta_673b1c1989(A);B[_C]=qube_b6b724ff27.sparta_e6aecc704c();return render(A,'dist/project/auth/registrationPending.html',B)
def sparta_ff137cbba5(request,token):
	A=request;B=qube_6059f885cd.sparta_34004cfd41(token)
	if int(B[_E])==1:C=B['user'];login(A,C);return redirect(_D)
	D=qube_b6b724ff27.sparta_673b1c1989(A);D[_C]=qube_b6b724ff27.sparta_e6aecc704c();return redirect(_I)
def sparta_49418591cd(request):logout(request);return redirect(_I)
def sparta_217d63d046(request):
	A=request
	if A.user.is_authenticated:
		if A.user.email=='cypress_tests@gmail.com':A.user.delete()
	logout(A);return redirect(_I)
def sparta_5ab1e346ad(request):A={_E:-100,_B:'You are not logged...'};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_069779294f(request):
	A=request;E='';F=_J
	if A.method==_K:
		B=ResetPasswordForm(A.POST)
		if B.is_valid():
			H=B.cleaned_data[_F];I=B.cleaned_data[_M];G=qube_6059f885cd.sparta_069779294f(H.lower(),I)
			try:
				if int(G[_E])==1:C=qube_b6b724ff27.sparta_673b1c1989(A);C.update(qube_b6b724ff27.sparta_2e9aa9b15f(A));B=ResetPasswordChangeForm(A.POST);C[_C]=qube_b6b724ff27.sparta_e6aecc704c();C[_G]=B;C[_F]=H;C[_H]=F;C[_B]=E;return render(A,_N,C)
				elif int(G[_E])==-1:E=G[_B];F=_A
			except Exception as J:print('exception ');print(J);E='Could not send reset email, please try again';F=_A
		else:E=_O;F=_A
	else:B=ResetPasswordForm()
	D=qube_b6b724ff27.sparta_673b1c1989(A);D.update(qube_b6b724ff27.sparta_2e9aa9b15f(A));D[_C]=qube_b6b724ff27.sparta_e6aecc704c();D[_G]=B;D[_H]=F;D[_B]=E;D.update(sparta_7c21b26e3e());return render(A,'dist/project/auth/resetPassword.html',D)
@csrf_exempt
def sparta_d213c3e808(request):
	D=request;E='';B=_J
	if D.method==_K:
		C=ResetPasswordChangeForm(D.POST)
		if C.is_valid():
			I=C.cleaned_data['token'];F=C.cleaned_data[_L];J=C.cleaned_data['password_confirmation'];K=C.cleaned_data[_M];G=C.cleaned_data[_F].lower()
			if len(F)<6:E='Your password must be at least 6 characters';B=_A
			if F!=J:E='The two passwords must be identical...';B=_A
			if not B:
				H=qube_6059f885cd.sparta_d213c3e808(K,I,G.lower(),F)
				try:
					if int(H[_E])==1:L=User.objects.get(username=G);login(D,L);return redirect(_D)
					else:E=H[_B];B=_A
				except Exception as M:E='Could not change your password, please try again';B=_A
		else:E=_O;B=_A
	else:return redirect('reset-password')
	A=qube_b6b724ff27.sparta_673b1c1989(D);A.update(qube_b6b724ff27.sparta_2e9aa9b15f(D));A[_C]=qube_b6b724ff27.sparta_e6aecc704c();A[_G]=C;A[_H]=B;A[_B]=E;A[_F]=G;A.update(sparta_7c21b26e3e());return render(D,_N,A)