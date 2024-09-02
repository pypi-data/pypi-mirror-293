from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 as qube_4982ec8d00
from project.models import UserProfile
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_091e7a614b
from project.sparta_83305eecd9.sparta_9659223ab2.qube_19c76c3c94 import sparta_f89886cc62
@sparta_091e7a614b
@login_required(redirect_field_name='login')
def sparta_e609f979b0(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A.update(qube_4982ec8d00.sparta_6204b13016(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_f89886cc62());return render(B,'dist/project/auth/settings.html',A)