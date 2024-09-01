_C='isAuth'
_B='jsonData'
_A='res'
import json
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from project.sparta_30e2c8fafc.sparta_4f7fa902d8 import qube_b0ccd99581 as qube_b0ccd99581
from project.sparta_9cf3fbfd16.sparta_527aa3c9b5.qube_8fc5e0b148 import sparta_a69f3c7c14
@csrf_exempt
def sparta_0cd5eb83b4(request):A=json.loads(request.body);B=json.loads(A[_B]);return qube_b0ccd99581.sparta_0cd5eb83b4(B)
@csrf_exempt
def sparta_6c7e0b8b5c(request):logout(request);A={_A:1};B=json.dumps(A);return HttpResponse(B)
@csrf_exempt
def sparta_ee32b8be35(request):
	if request.user.is_authenticated:A=1
	else:A=0
	B={_A:1,_C:A};C=json.dumps(B);return HttpResponse(C)
def sparta_c6dcea37ef(request):
	B=request;from django.contrib.auth import authenticate as F,login;from django.contrib.auth.models import User as C;G=json.loads(B.body);D=json.loads(G[_B]);H=D['email'];I=D['password'];E=0
	try:
		A=C.objects.get(email=H);A=F(B,username=A.username,password=I)
		if A is not None:login(B,A);E=1
	except C.DoesNotExist:pass
	J={_A:1,_C:E};K=json.dumps(J);return HttpResponse(K)