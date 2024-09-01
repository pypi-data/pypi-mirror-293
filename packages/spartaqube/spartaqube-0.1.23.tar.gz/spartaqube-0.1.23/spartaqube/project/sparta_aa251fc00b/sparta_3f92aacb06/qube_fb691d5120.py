from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_9cf3fbfd16.sparta_527aa3c9b5.qube_8fc5e0b148 as qube_8fc5e0b148
from project.models import UserProfile
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_7e621e226c
from project.sparta_aa251fc00b.sparta_b156cb6dcc.qube_10ae3eaa29 import sparta_e52b0fd9c2
@sparta_7e621e226c
@login_required(redirect_field_name='login')
def sparta_99a9c2cc96(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_8fc5e0b148.sparta_5c9f39e944(B);A.update(qube_8fc5e0b148.sparta_31ee8ccaef(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_e52b0fd9c2());return render(B,'dist/project/auth/settings.html',A)