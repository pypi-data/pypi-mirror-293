from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_c8e521c5f3.sparta_bc89190359.qube_6059f885cd import sparta_25d3a2863e
from project.sparta_c8e521c5f3.sparta_b71700fcc2 import qube_b0b9718cd8 as qube_b0b9718cd8
from project.models import UserProfile
import project.sparta_3ca0064d9b.sparta_e277eee10c.qube_b6b724ff27 as qube_b6b724ff27
@sparta_25d3a2863e
@login_required(redirect_field_name='login')
def sparta_766ee8be40(request):
	E='avatarImg';B=request;A=qube_b6b724ff27.sparta_673b1c1989(B);A['menuBar']=-1;F=qube_b6b724ff27.sparta_20838164ba(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_25d3a2863e
@login_required(redirect_field_name='login')
def sparta_c067890279(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_766ee8be40(A)