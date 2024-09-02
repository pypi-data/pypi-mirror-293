from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_40ba2b27bc.sparta_5da2ea1aa8.qube_816b9a59f8 import sparta_42f3fead5c
from project.sparta_40ba2b27bc.sparta_f1aa1afeb1 import qube_de9a3677f3 as qube_de9a3677f3
from project.models import UserProfile
import project.sparta_d7b94e3744.sparta_cc6e9d39f9.qube_707ef4ff5f as qube_707ef4ff5f
@sparta_42f3fead5c
@login_required(redirect_field_name='login')
def sparta_f908558b1d(request):
	E='avatarImg';B=request;A=qube_707ef4ff5f.sparta_d9406e4da5(B);A['menuBar']=-1;F=qube_707ef4ff5f.sparta_d157c2d07e(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_42f3fead5c
@login_required(redirect_field_name='login')
def sparta_9dff586837(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_f908558b1d(A)