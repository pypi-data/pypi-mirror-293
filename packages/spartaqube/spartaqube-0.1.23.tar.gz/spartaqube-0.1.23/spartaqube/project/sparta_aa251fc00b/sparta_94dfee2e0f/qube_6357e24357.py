from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_30e2c8fafc.sparta_4f7fa902d8.qube_b0ccd99581 import sparta_7e621e226c
from project.sparta_30e2c8fafc.sparta_dc1e3836d5 import qube_b1cef934b3 as qube_b1cef934b3
from project.models import UserProfile
import project.sparta_9cf3fbfd16.sparta_527aa3c9b5.qube_8fc5e0b148 as qube_8fc5e0b148
@sparta_7e621e226c
@login_required(redirect_field_name='login')
def sparta_f91612aecf(request):
	E='avatarImg';B=request;A=qube_8fc5e0b148.sparta_5c9f39e944(B);A['menuBar']=-1;F=qube_8fc5e0b148.sparta_31ee8ccaef(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_7e621e226c
@login_required(redirect_field_name='login')
def sparta_54b74f1737(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_f91612aecf(A)