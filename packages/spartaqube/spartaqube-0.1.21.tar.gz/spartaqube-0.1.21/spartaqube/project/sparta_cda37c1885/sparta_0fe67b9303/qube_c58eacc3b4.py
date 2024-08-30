from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b as qube_cb1c81c00b
from project.models import UserProfile
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_43a7ace2a8
from project.sparta_cda37c1885.sparta_dd728ae143.qube_c0d36a3834 import sparta_5dad476a0c
@sparta_43a7ace2a8
@login_required(redirect_field_name='login')
def sparta_1ae1e9936f(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A.update(qube_cb1c81c00b.sparta_abf92cd2d9(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_5dad476a0c());return render(B,'dist/project/auth/settings.html',A)