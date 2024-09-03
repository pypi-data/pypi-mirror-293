from urllib.parse import urlparse,urlunparse
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf_settings
from django.shortcuts import render
import project.sparta_3ca0064d9b.sparta_e277eee10c.qube_b6b724ff27 as qube_b6b724ff27
from project.models import UserProfile
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_25d3a2863e
from project.sparta_b9d232118a.sparta_8fbf22c2b0.qube_59aa161eb3 import sparta_7c21b26e3e
@sparta_25d3a2863e
@login_required(redirect_field_name='login')
def sparta_19ce7e7d55(request,idSection=1):
	B=request;D=UserProfile.objects.get(user=B.user);E=D.avatar
	if E is not None:E=D.avatar.avatar
	C=urlparse(conf_settings.URL_TERMS)
	if not C.scheme:C=urlunparse(C._replace(scheme='http'))
	F={'item':1,'idSection':idSection,'userProfil':D,'avatar':E,'url_terms':C};A=qube_b6b724ff27.sparta_673b1c1989(B);A.update(qube_b6b724ff27.sparta_20838164ba(B.user));A.update(F);G='';A['accessKey']=G;A.update(sparta_7c21b26e3e());return render(B,'dist/project/auth/settings.html',A)