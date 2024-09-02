from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_d7b94e3744.sparta_cc6e9d39f9.qube_707ef4ff5f as qube_707ef4ff5f
from project.models import UserProfile
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_42f3fead5c
from project.sparta_55af41a040.sparta_6b616e1326.qube_df717acb9e import sparta_dc31a2f3a5
@sparta_42f3fead5c
@login_required(redirect_field_name='login')
def sparta_7b9c8b107f(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_707ef4ff5f.sparta_d9406e4da5(B);A.update(qube_707ef4ff5f.sparta_d157c2d07e(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_dc31a2f3a5());return render(B,'dist/project/auth/settings.html',A)