from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_55934fbdfb.sparta_db8b2eb16f.qube_da95fe36a3 import sparta_091e7a614b
from project.sparta_55934fbdfb.sparta_2c7485b6ab import qube_0f88a22cae as qube_0f88a22cae
from project.models import UserProfile
import project.sparta_b972c86658.sparta_741716a68d.qube_4982ec8d00 as qube_4982ec8d00
@sparta_091e7a614b
@login_required(redirect_field_name='login')
def sparta_a497944a32(request):
	E='avatarImg';B=request;A=qube_4982ec8d00.sparta_48cfdf4b1d(B);A['menuBar']=-1;F=qube_4982ec8d00.sparta_6204b13016(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_091e7a614b
@login_required(redirect_field_name='login')
def sparta_a106ef470f(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_a497944a32(A)