from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from project.sparta_12b080e841.sparta_0687762cca.qube_90b70a692d import sparta_43a7ace2a8
from project.sparta_12b080e841.sparta_12a15bb49c import qube_3347c14f73 as qube_3347c14f73
from project.models import UserProfile
import project.sparta_509f9a5b62.sparta_76f284387c.qube_cb1c81c00b as qube_cb1c81c00b
@sparta_43a7ace2a8
@login_required(redirect_field_name='login')
def sparta_3bbf7cd69a(request):
	E='avatarImg';B=request;A=qube_cb1c81c00b.sparta_aca8f1d9a9(B);A['menuBar']=-1;F=qube_cb1c81c00b.sparta_abf92cd2d9(B.user);A.update(F);A[E]='';C=UserProfile.objects.filter(user=B.user)
	if C.count()>0:
		D=C[0];G=D.avatar
		if G is not None:H=D.avatar.image64;A[E]=H
	A['bInvertIcon']=0;return render(B,'dist/project/helpCenter/helpCenter.html',A)
@sparta_43a7ace2a8
@login_required(redirect_field_name='login')
def sparta_96a525e426(request):
	A=request;B=UserProfile.objects.filter(user=A.user)
	if B.count()>0:C=B[0];C.has_open_tickets=False;C.save()
	return sparta_3bbf7cd69a(A)